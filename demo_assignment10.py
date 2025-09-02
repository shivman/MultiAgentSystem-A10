#!/usr/bin/env python3
"""
Assignment 10 Demo Script
Demonstrates all the new features including human-in-the-loop, 
max steps/retries enforcement, and tool performance logging.
"""

import asyncio
import json
import time
from agent.agent_loop2 import AgentLoop
from mcp_servers.multiMCP import MultiMCP
import yaml

class Assignment10Demo:
    def __init__(self):
        self.agent = None
        
    async def initialize(self):
        """Initialize the agent for demo"""
        print("🚀 Initializing Assignment 10 Demo...")
        
        with open("config/mcp_server_config.yaml", "r") as f:
            profile = yaml.safe_load(f)
            mcp_servers_list = profile.get("mcp_servers", [])
            configs = list(mcp_servers_list)

        multi_mcp = MultiMCP(server_configs=configs)
        await multi_mcp.initialize()
        
        self.agent = AgentLoop(
            perception_prompt_path="prompts/perception_prompt.txt",
            decision_prompt_path="prompts/decision_prompt.txt",
            multi_mcp=multi_mcp,
            strategy="exploratory"
        )
        print("✅ Agent initialized for demo")

    async def demo_feature_1_tool_failure(self):
        """Demo: Human-in-the-Loop for Tool Failures"""
        print("\n" + "="*60)
        print("🎭 DEMO 1: Human-in-the-Loop for Tool Failures")
        print("="*60)
        print("This demo will show how the system handles tool failures")
        print("and prompts for human intervention.")
        
        query = "Divide by zero and calculate the square root of -1"
        print(f"\nQuery: {query}")
        print("This query will cause tool failures and trigger human intervention.")
        
        input("\nPress Enter to continue...")
        
        session = await self.agent.run(query)
        
        print(f"\n✅ Demo 1 completed!")
        print(f"Steps executed: {self.agent.step_count}")
        print(f"Retries used: {self.agent.retry_count}")

    async def demo_feature_2_plan_failure(self):
        """Demo: Human-in-the-Loop for Plan Failures"""
        print("\n" + "="*60)
        print("🎭 DEMO 2: Human-in-the-Loop for Plan Failures")
        print("="*60)
        print("This demo will show how the system handles plan failures")
        print("when max steps are reached.")
        
        query = "Calculate factorial of 10, then find square root, then multiply by 5, then add 100, then divide by 2, then find the cube root, then multiply by 3"
        print(f"\nQuery: {query}")
        print("This complex query will reach max steps and trigger human intervention.")
        
        input("\nPress Enter to continue...")
        
        session = await self.agent.run(query)
        
        print(f"\n✅ Demo 2 completed!")
        print(f"Steps executed: {self.agent.step_count}")
        print(f"Max steps reached: {self.agent.step_count >= 3}")

    async def demo_feature_3_tool_performance(self):
        """Demo: Tool Performance Logging"""
        print("\n" + "="*60)
        print("🎭 DEMO 3: Tool Performance Logging")
        print("="*60)
        print("This demo will show tool performance tracking.")
        
        # Run several queries to generate tool usage
        queries = [
            "Calculate 5 + 3",
            "Find the factorial of 4", 
            "Calculate 2 to the power of 8",
            "Calculate 10 / 2",
            "Find the square root of 16"
        ]
        
        print("Running multiple queries to generate tool performance data...")
        
        for i, query in enumerate(queries, 1):
            print(f"\nQuery {i}: {query}")
            await self.agent.run(query)
            await asyncio.sleep(1)  # Small delay between queries
        
        print(f"\n✅ Demo 3 completed!")
        print("Tool performance data has been logged.")
        
        # Show tool performance
        if hasattr(self.agent, 'tool_performance_log'):
            print("\n📊 Tool Performance Summary:")
            for tool_name, stats in self.agent.tool_performance_log.items():
                if stats['total_calls'] > 0:
                    success_rate = (stats['successful_calls'] / stats['total_calls']) * 100
                    print(f"  {tool_name}: {success_rate:.1f}% success rate ({stats['total_calls']} calls)")

    async def demo_feature_4_max_limits(self):
        """Demo: Max Steps and Retries Enforcement"""
        print("\n" + "="*60)
        print("🎭 DEMO 4: Max Steps and Retries Enforcement")
        print("="*60)
        print("This demo will show the enforcement of max steps and retries.")
        
        # Reset agent counters
        self.agent.step_count = 0
        self.agent.retry_count = 0
        
        print("Testing max steps enforcement...")
        query = "Calculate factorial of 10, then find square root, then multiply by 5, then add 100"
        print(f"Query: {query}")
        
        session = await self.agent.run(query)
        
        print(f"\n✅ Demo 4 completed!")
        print(f"Max steps (3) enforced: {self.agent.step_count >= 3}")
        print(f"Steps executed: {self.agent.step_count}")

    async def demo_feature_5_reliability_scoring(self):
        """Demo: Tool Reliability Scoring"""
        print("\n" + "="*60)
        print("🎭 DEMO 5: Tool Reliability Scoring")
        print("="*60)
        print("This demo will show tool reliability scoring.")
        
        # Test reliability scores for different tools
        test_tools = ["add", "factorial", "power", "nonexistent_tool"]
        
        print("Testing reliability scores for various tools:")
        for tool in test_tools:
            score = self.agent.get_tool_reliability_score(tool)
            print(f"  {tool}: {score:.3f}")
        
        print(f"\n✅ Demo 5 completed!")

    async def run_full_demo(self):
        """Run the complete Assignment 10 demo"""
        print("🎬 ASSIGNMENT 10 FEATURE DEMO")
        print("="*60)
        print("This demo showcases all the new features:")
        print("1. Human-in-the-Loop for Tool Failures")
        print("2. Human-in-the-Loop for Plan Failures") 
        print("3. Tool Performance Logging")
        print("4. Max Steps and Retries Enforcement")
        print("5. Tool Reliability Scoring")
        print("="*60)
        
        await self.initialize()
        
        # Run all demos
        await self.demo_feature_1_tool_failure()
        await self.demo_feature_2_plan_failure()
        await self.demo_feature_3_tool_performance()
        await self.demo_feature_4_max_limits()
        await self.demo_feature_5_reliability_scoring()
        
        print("\n" + "="*60)
        print("🎉 ASSIGNMENT 10 DEMO COMPLETED!")
        print("="*60)
        print("All features have been demonstrated successfully.")
        print("Check the generated files for detailed results:")
        print("- tool_performance_log.json")
        print("- Any simulation results files")
        
        # Save demo summary
        self.save_demo_summary()

    def save_demo_summary(self):
        """Save demo summary to file"""
        summary = {
            "demo_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "features_demonstrated": [
                "Human-in-the-Loop for Tool Failures",
                "Human-in-the-Loop for Plan Failures", 
                "Tool Performance Logging",
                "Max Steps and Retries Enforcement",
                "Tool Reliability Scoring"
            ],
            "tool_performance": self.agent.tool_performance_log if hasattr(self.agent, 'tool_performance_log') else {},
            "max_steps": 3,
            "max_retries": 3
        }
        
        filename = f"demo_summary_{time.strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n💾 Demo summary saved to: {filename}")

async def main():
    """Main function to run the demo"""
    demo = Assignment10Demo()
    await demo.run_full_demo()

if __name__ == "__main__":
    asyncio.run(main())
