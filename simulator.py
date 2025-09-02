import asyncio
import json
import time
import random
from datetime import datetime
from agent.agent_loop2 import AgentLoop
from mcp_servers.multiMCP import MultiMCP
import yaml

class AgentSimulator:
    def __init__(self, config_path="config/mcp_server_config.yaml"):
        self.config_path = config_path
        self.test_results = []
        self.load_test_queries()
        
    def load_test_queries(self):
        """Load predefined test queries"""
        self.test_queries = [
            # Math operations
            "What is 15 + 27?",
            "Calculate the factorial of 5",
            "What is the square root of 144?",
            "Calculate 2 to the power of 10",
            
            # Document operations
            "Search for information about cricket in the documents",
            "Extract text from the PDF files",
            "Find documents related to Tesla",
            
            # Web search operations
            "Search for the latest news about AI",
            "Find information about Python programming",
            "Search for machine learning tutorials",
            
            # Complex queries
            "Calculate the fibonacci sequence up to 10 numbers",
            "What is the weather like today?",
            "Find the population of New York City",
            "Calculate the area of a circle with radius 5",
            
            # Error-prone queries (to test failure handling)
            "Divide by zero",
            "Access a non-existent file",
            "Call an undefined function",
            "Calculate the square root of -1",
            
            # Multi-step queries
            "Calculate 5 factorial and then add 10 to the result",
            "Find the sum of first 10 natural numbers and multiply by 2",
            "Calculate the area of a rectangle with length 5 and width 3, then find its perimeter",
            
            # Document analysis
            "Analyze the content of the economic document",
            "Extract key points from the Tesla document",
            "Summarize the DLF document",
            
            # Mixed operations
            "Search for AI news and calculate how many results were found",
            "Find documents about Tesla and count the total pages",
            "Calculate the average of numbers 1 to 10 and search for related information"
        ]
        
        # Add more variations
        for i in range(50):
            base_queries = [
                f"Calculate {random.randint(1, 100)} + {random.randint(1, 100)}",
                f"Find the factorial of {random.randint(1, 10)}",
                f"Calculate {random.randint(2, 20)} to the power of {random.randint(2, 5)}",
                f"Search for information about topic {i}",
                f"Analyze document number {i}",
                f"Calculate the area of a circle with radius {random.randint(1, 20)}",
                f"Find the sum of first {random.randint(5, 20)} natural numbers",
                f"Calculate fibonacci sequence up to {random.randint(5, 15)} numbers"
            ]
            self.test_queries.extend(base_queries)
    
    async def initialize_agent(self):
        """Initialize the agent with MCP servers"""
        print("Initializing MCP Servers...")
        with open(self.config_path, "r") as f:
            profile = yaml.safe_load(f)
            mcp_servers_list = profile.get("mcp_servers", [])
            configs = list(mcp_servers_list)

        # Initialize MCP + Dispatcher
        multi_mcp = MultiMCP(server_configs=configs)
        await multi_mcp.initialize()
        
        self.agent = AgentLoop(
            perception_prompt_path="prompts/perception_prompt.txt",
            decision_prompt_path="prompts/decision_prompt.txt",
            multi_mcp=multi_mcp,
            strategy="exploratory"
        )
        print("✅ Agent initialized successfully")
    
    async def run_single_test(self, query: str, test_id: int) -> dict:
        """Run a single test with the agent"""
        print(f"\n{'='*60}")
        print(f"🧪 Test #{test_id}: {query}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        try:
            # Run the agent
            session = await self.agent.run(query)
            
            execution_time = time.time() - start_time
            
            # Extract results
            result = {
                "test_id": test_id,
                "query": query,
                "execution_time": execution_time,
                "success": session.state.get("original_goal_achieved", False),
                "final_answer": session.state.get("final_answer", "No answer"),
                "confidence": session.state.get("confidence", 0.0),
                "step_count": self.agent.step_count,
                "retry_count": self.agent.retry_count,
                "plan_versions": len(session.plan_versions),
                "session_id": session.session_id,
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"✅ Test #{test_id} completed in {execution_time:.2f}s")
            print(f"Success: {result['success']}")
            print(f"Steps: {result['step_count']}")
            print(f"Retries: {result['retry_count']}")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Test #{test_id} failed: {str(e)}")
            
            return {
                "test_id": test_id,
                "query": query,
                "execution_time": execution_time,
                "success": False,
                "error": str(e),
                "final_answer": "Error occurred",
                "confidence": 0.0,
                "step_count": 0,
                "retry_count": 0,
                "plan_versions": 0,
                "session_id": f"error_{test_id}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def run_simulation(self, num_tests: int = 100, sleep_between_tests: float = 2.0):
        """Run the full simulation"""
        print(f"🚀 Starting Agent Simulation")
        print(f"Total tests: {num_tests}")
        print(f"Sleep between tests: {sleep_between_tests}s")
        
        # Initialize agent
        await self.initialize_agent()
        
        # Run tests
        for i in range(min(num_tests, len(self.test_queries))):
            query = self.test_queries[i]
            result = await self.run_single_test(query, i + 1)
            self.test_results.append(result)
            
            # Sleep to avoid rate limiting
            if i < num_tests - 1:  # Don't sleep after the last test
                print(f"😴 Sleeping for {sleep_between_tests}s...")
                await asyncio.sleep(sleep_between_tests)
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate a comprehensive test report"""
        print(f"\n{'='*60}")
        print(f"📊 SIMULATION REPORT")
        print(f"{'='*60}")
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r['success'])
        failed_tests = total_tests - successful_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(successful_tests/total_tests)*100:.2f}%")
        
        # Average execution time
        avg_time = sum(r['execution_time'] for r in self.test_results) / total_tests
        print(f"Average Execution Time: {avg_time:.2f}s")
        
        # Step analysis
        total_steps = sum(r['step_count'] for r in self.test_results)
        avg_steps = total_steps / total_tests
        print(f"Total Steps: {total_steps}")
        print(f"Average Steps per Test: {avg_steps:.2f}")
        
        # Retry analysis
        total_retries = sum(r['retry_count'] for r in self.test_results)
        avg_retries = total_retries / total_tests
        print(f"Total Retries: {total_retries}")
        print(f"Average Retries per Test: {avg_retries:.2f}")
        
        # Tool performance analysis
        if hasattr(self.agent, 'tool_performance_log'):
            print(f"\n🔧 Tool Performance:")
            for tool_name, stats in self.agent.tool_performance_log.items():
                if stats['total_calls'] > 0:
                    success_rate = (stats['successful_calls'] / stats['total_calls']) * 100
                    print(f"  {tool_name}: {success_rate:.1f}% success rate ({stats['total_calls']} calls)")
        
        # Save detailed results
        self.save_results()
    
    def save_results(self):
        """Save test results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"simulation_results_{timestamp}.json"
        
        report = {
            "simulation_metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_tests": len(self.test_results),
                "successful_tests": sum(1 for r in self.test_results if r['success']),
                "failed_tests": sum(1 for r in self.test_results if not r['success']),
                "success_rate": (sum(1 for r in self.test_results if r['success']) / len(self.test_results)) * 100
            },
            "tool_performance": self.agent.tool_performance_log if hasattr(self.agent, 'tool_performance_log') else {},
            "test_results": self.test_results
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")

async def main():
    """Main function to run the simulation"""
    simulator = AgentSimulator()
    
    # Run simulation with 100 tests and 2 second sleep
    await simulator.run_simulation(num_tests=100, sleep_between_tests=2.0)

if __name__ == "__main__":
    asyncio.run(main())
