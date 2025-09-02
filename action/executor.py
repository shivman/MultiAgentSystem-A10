
import ast
import asyncio
import time
import builtins
import textwrap
import re
from datetime import datetime

# ───────────────────────────────────────────────────────────────
# CONFIG
# ───────────────────────────────────────────────────────────────
ALLOWED_MODULES = {
    "math", "cmath", "decimal", "fractions", "random", "statistics", "itertools", "functools", "operator", "string", "re", "datetime", "calendar", "time", "collections", "heapq", "bisect", "types", "copy", "enum", "uuid", "dataclasses", "typing", "pprint", "json", "base64", "hashlib", "hmac", "secrets", "struct", "zlib", "gzip", "bz2", "lzma", "io", "pathlib", "tempfile", "textwrap", "difflib", "unicodedata", "html", "html.parser", "xml", "xml.etree.ElementTree", "csv", "sqlite3", "contextlib", "traceback", "ast", "tokenize", "token", "builtins"
}
MAX_FUNCTIONS = 5
TIMEOUT_PER_FUNCTION = 500  # seconds

class KeywordStripper(ast.NodeTransformer):
    """Rewrite all function calls to remove keyword args and keep only values as positional."""
    def visit_Call(self, node):
        self.generic_visit(node)
        if node.keywords:
            # Convert all keyword arguments into positional args (discard names)
            for kw in node.keywords:
                node.args.append(kw.value)
            node.keywords = []
        return node


# ───────────────────────────────────────────────────────────────
# AST TRANSFORMER: auto-await known async MCP tools
# ───────────────────────────────────────────────────────────────
class AwaitTransformer(ast.NodeTransformer):
    def __init__(self, async_funcs):
        self.async_funcs = async_funcs

    def visit_Call(self, node):
        self.generic_visit(node)
        # Only wrap with await if the function is actually async
        if isinstance(node.func, ast.Name) and node.func.id in self.async_funcs:
            # Check if the function is actually async by looking at the function object
            func_obj = self.async_funcs.get(node.func.id)
            if func_obj and asyncio.iscoroutinefunction(func_obj):
                return ast.Await(value=node)
        return node

# ───────────────────────────────────────────────────────────────
# UTILITY FUNCTIONS
# ───────────────────────────────────────────────────────────────
def count_function_calls(code: str) -> int:
    tree = ast.parse(code)
    return sum(isinstance(node, ast.Call) for node in ast.walk(tree))

def build_safe_globals(mcp_funcs: dict, multi_mcp=None) -> dict:
    safe_globals = {
        "__builtins__": {
            k: getattr(builtins, k)
            for k in ("range", "len", "int", "float", "str", "list", "dict", "print", "sum", "__import__", "isinstance", "hasattr")
        },
        **mcp_funcs,
    }

    for module in ALLOWED_MODULES:
        safe_globals[module] = __import__(module)

    # Store LLM-style result
    safe_globals["final_answer"] = lambda x: safe_globals.setdefault("result_holder", x)

    # Optional: add parallel execution
    if multi_mcp:
        async def parallel(*tool_calls):
            coros = [
                multi_mcp.function_wrapper(tool_name, *args)
                for tool_name, *args in tool_calls
            ]
            return await asyncio.gather(*coros)

        safe_globals["parallel"] = parallel

    return safe_globals


# ───────────────────────────────────────────────────────────────
# MAIN EXECUTOR
# ───────────────────────────────────────────────────────────────
async def run_user_code(code: str, multi_mcp) -> dict:
    start_time = time.perf_counter()
    start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        func_count = count_function_calls(code)
        if func_count > MAX_FUNCTIONS:
            return {
                "status": "error",
                "error": f"Too many functions ({func_count} > {MAX_FUNCTIONS})",
                "execution_time": start_timestamp,
                "total_time": str(round(time.perf_counter() - start_time, 3))
            }

        tool_funcs = {
            tool.name: make_tool_proxy(tool.name, multi_mcp)
            for tool in multi_mcp.get_all_tools()
        }

        sandbox = build_safe_globals(tool_funcs, multi_mcp)
        local_vars = {}

        cleaned_code = textwrap.dedent(code.strip())
        
        # Check for common variable scope violations before parsing
        scope_violations = [
            "completed_steps", "execution_result", "previous_step", "step_result",
            "session", "plan_versions", "current_plan"
        ]
        
        for violation in scope_violations:
            if violation in cleaned_code:
                return {
                    "status": "error",
                    "error": f"Variable scope violation detected: '{violation}' is not allowed. Each step must be self-contained and cannot reference previous step results or session state.",
                    "execution_time": start_timestamp,
                    "total_time": str(round(time.perf_counter() - start_time, 3))
                }
        
        tree = ast.parse(cleaned_code)

        has_return = any(isinstance(node, ast.Return) for node in tree.body)
        has_result = any(
            isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "result" for t in node.targets
            )
            for node in tree.body
        )
        if not has_return and has_result:
            tree.body.append(ast.Return(value=ast.Name(id="result", ctx=ast.Load())))

        tree = KeywordStripper().visit(tree) # strip "key" = "value" cases to only "value"
        tree = AwaitTransformer(tool_funcs).visit(tree)
        ast.fix_missing_locations(tree)

        func_def = ast.AsyncFunctionDef(
            name="__main",
            args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
            body=tree.body,
            decorator_list=[]
        )
        wrapper = ast.Module(body=[func_def], type_ignores=[])
        ast.fix_missing_locations(wrapper)

        compiled = compile(wrapper, filename="<user_code>", mode="exec")
        exec(compiled, sandbox, local_vars)

        try:
            timeout = max(3, func_count * TIMEOUT_PER_FUNCTION)  # minimum 3s even for plain returns
            returned = await asyncio.wait_for(local_vars["__main"](), timeout=timeout)

            result_value = returned if returned is not None else sandbox.get("result_holder", "None")

            # If result looks like tool error text, extract
            # Handle CallToolResult errors from MCP
            if hasattr(result_value, "isError") and getattr(result_value, "isError", False):
                error_msg = None

                try:
                    error_msg = result_value.content[0].text.strip()
                except Exception:
                    error_msg = str(result_value)

                return {
                    "status": "error",
                    "error": error_msg,
                    "execution_time": start_timestamp,
                    "total_time": str(round(time.perf_counter() - start_time, 3))
                }

            # Else: normal success
            return {
                "status": "success",
                "result": str(result_value),
                "execution_time": start_timestamp,
                "total_time": str(round(time.perf_counter() - start_time, 3))
            }


        except Exception as e:
            error_msg = str(e)
            # Check for common variable scope errors
            if "name" in error_msg.lower() and "is not defined" in error_msg:
                error_msg = f"Variable scope error: {error_msg}. Variables from previous steps are not accessible. Each step must be self-contained."
            elif "completed_steps" in error_msg.lower() or "execution_result" in error_msg.lower():
                error_msg = f"Variable scope error: {error_msg}. Each step must be self-contained and cannot reference previous step results."
            elif "keyerror" in error_msg.lower():
                error_msg = f"Data structure error: {error_msg}. The expected data structure was not found or was empty. Please check the data structure returned by the tool."
            elif "indexerror" in error_msg.lower():
                error_msg = f"Index error: {error_msg}. The requested index is out of range or the data structure is empty."
            
            return {
                "status": "error",
                "error": f"{type(e).__name__}: {error_msg}",
                "execution_time": start_timestamp,
                "total_time": str(round(time.perf_counter() - start_time, 3))
            }


    except asyncio.TimeoutError:
        return {
            "status": "error",
            "error": f"Execution timed out after {func_count * TIMEOUT_PER_FUNCTION} seconds",
            "execution_time": start_timestamp,
            "total_time": str(round(time.perf_counter() - start_time, 3))
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "execution_time": start_timestamp,
            "total_time": str(round(time.perf_counter() - start_time, 3))
        }

# ───────────────────────────────────────────────────────────────
# TOOL WRAPPER
# ───────────────────────────────────────────────────────────────
def make_tool_proxy(tool_name: str, mcp):
    async def _tool_fn(*args):
        return await mcp.function_wrapper(tool_name, *args)
    return _tool_fn