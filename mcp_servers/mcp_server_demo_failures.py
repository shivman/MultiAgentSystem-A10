from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from mcp import types
import random
import time

mcp = FastMCP("DemoFailureTool")

# Demo failure tool for YouTube demonstrations
@mcp.tool()
def artificial_failure(input: str) -> str:
    """Artificially fail for demonstration purposes. Always fails with different error types."""
    print("CALLED: artificial_failure - This will always fail for demo purposes")
    
    # Random failure types for variety
    failure_types = [
        "Connection timeout error",
        "Permission denied error", 
        "Resource not found error",
        "Invalid parameter error",
        "Rate limit exceeded error",
        "Authentication failed error",
        "Network unreachable error",
        "File system error",
        "Memory allocation error",
        "Database connection error"
    ]
    
    error_type = random.choice(failure_types)
    raise Exception(f"DEMO FAILURE: {error_type} - {input}")

@mcp.tool()
def conditional_failure(input: str, should_fail: bool = True) -> str:
    """Conditionally fail based on parameter. Useful for controlled demos."""
    print(f"CALLED: conditional_failure - should_fail={should_fail}")
    
    if should_fail:
        raise Exception(f"DEMO FAILURE: Conditional failure triggered - {input}")
    else:
        return f"SUCCESS: {input} processed successfully"

@mcp.tool()
def delayed_failure(input: str, delay_seconds: int = 2) -> str:
    """Fail after a delay to simulate timeout scenarios."""
    print(f"CALLED: delayed_failure - will fail after {delay_seconds} seconds")
    
    time.sleep(delay_seconds)
    raise Exception(f"DEMO FAILURE: Timeout after {delay_seconds} seconds - {input}")

@mcp.tool()
def random_success_failure(input: str) -> str:
    """Randomly succeed or fail for testing reliability."""
    print("CALLED: random_success_failure - random outcome")
    
    if random.random() < 0.3:  # 30% success rate
        return f"SUCCESS: {input} processed successfully"
    else:
        raise Exception(f"DEMO FAILURE: Random failure - {input}")

if __name__ == "__main__":
    mcp.run()
