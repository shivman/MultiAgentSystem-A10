#!/usr/bin/env python3
"""
YouTube Demo Scripts for Human-in-the-Loop System
Demonstrates tool failures, step failures, and human intervention capabilities
"""

import asyncio
import json
import time
from datetime import datetime
from agent.agent_loop2 import AgentLoop
from mcp_servers.multiMCP import MultiMCP
import yaml

class YouTubeDemoScripts:
    def __init__(self):
        self.agent = None
        self.demo_results = []
        
    async def initialize_agent(self):
        """Initialize the agent for demos"""
        print("🚀 Initializing Agent for YouTube Demos...")
        
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
        print("✅ Agent initialized for demos")

    async def demo_1_tool_failure_division_by_zero(self):
        """Demo 1: Tool Failure - Division by Zero"""
        print("\n" + "="*80)
        print("🎬 YOUTUBE DEMO 1: Tool Failure - Division by Zero")
        print("="*80)
        print("📝 Script: This demo shows how the system handles division by zero")
        print("   and triggers human-in-the-loop intervention.")
        
        query = "Divide 10 by 0 and then calculate the square root of -1"
        print(f"\n🔍 Query: {query}")
        print("\n📋 Expected Behavior:")
        print("   1. The 'divide' tool will fail with 'division by zero' error")
        print("   2. System will trigger human-in-the-loop intervention")
        print("   3. User will be prompted with 4 options:")
        print("      - Suggest alternative approach")
        print("      - Provide manual result")
        print("      - Skip this step")
        print("      - Retry with different parameters")
        
        print("\n🎥 Recording Tips:")
        print("   - Show the error message clearly")
        print("   - Demonstrate each of the 4 human intervention options")
        print("   - Show how human guidance resolves the failure")
        
        input("\n⏸️  Press Enter to start the demo...")
        
        start_time = time.time()
        session = await self.agent.run(query)
        execution_time = time.time() - start_time
        
        result = {
            "demo_id": 1,
            "title": "Tool Failure - Division by Zero",
            "query": query,
            "execution_time": execution_time,
            "steps_executed": self.agent.step_count,
            "retries_used": self.agent.retry_count,
            "human_interventions": self.agent.retry_count,
            "success": session.state.get("original_goal_achieved", False),
            "timestamp": datetime.now().isoformat()
        }
        
        self.demo_results.append(result)
        print(f"\n✅ Demo 1 completed in {execution_time:.2f}s")
        print(f"   Steps: {result['steps_executed']}, Retries: {result['retries_used']}")
        
        return result

    async def demo_2_step_failure_max_steps(self):
        """Demo 2: Step Failure - Max Steps Reached"""
        print("\n" + "="*80)
        print("🎬 YOUTUBE DEMO 2: Step Failure - Max Steps Reached")
        print("="*80)
        print("📝 Script: This demo shows how the system handles complex queries")
        print("   that exceed the maximum step limit (3 steps).")
        
        query = "Calculate factorial of 10, then find square root, then multiply by 5, then add 100, then divide by 2, then find cube root, then calculate sine of result"
        print(f"\n🔍 Query: {query}")
        print("\n📋 Expected Behavior:")
        print("   1. Query requires more than 3 steps (MAX_STEPS = 3)")
        print("   2. System will reach max steps limit")
        print("   3. Human-in-the-loop will be triggered for plan failure")
        print("   4. User will be prompted with 4 options:")
        print("      - Provide new plan steps")
        print("      - Modify existing plan")
        print("      - Provide direct answer")
        print("      - Start over with different approach")
        
        print("\n🎥 Recording Tips:")
        print("   - Show the step counter reaching 3")
        print("   - Demonstrate plan failure intervention")
        print("   - Show how human guidance modifies the plan")
        
        input("\n⏸️  Press Enter to start the demo...")
        
        start_time = time.time()
        session = await self.agent.run(query)
        execution_time = time.time() - start_time
        
        result = {
            "demo_id": 2,
            "title": "Step Failure - Max Steps Reached",
            "query": query,
            "execution_time": execution_time,
            "steps_executed": self.agent.step_count,
            "retries_used": self.agent.retry_count,
            "human_interventions": 1,  # Plan failure intervention
            "success": session.state.get("original_goal_achieved", False),
            "timestamp": datetime.now().isoformat()
        }
        
        self.demo_results.append(result)
        print(f"\n✅ Demo 2 completed in {execution_time:.2f}s")
        print(f"   Steps: {result['steps_executed']}, Retries: {result['retries_used']}")
        
        return result

    async def demo_3_success_case(self):
        """Demo 3: Success Case - Normal Operation"""
        print("\n" + "="*80)
        print("🎬 YOUTUBE DEMO 3: Success Case - Normal Operation")
        print("="*80)
        print("📝 Script: This demo shows normal operation without human intervention.")
        
        query = "Calculate 5 factorial and then add 10 to the result"
        print(f"\n🔍 Query: {query}")
        print("\n📋 Expected Behavior:")
        print("   1. Step 1: Calculate factorial of 5 (120)")
        print("   2. Step 2: Add 10 to result (130)")
        print("   3. Query completes successfully within 3 steps")
        print("   4. No human intervention required")
        
        print("\n🎥 Recording Tips:")
        print("   - Show smooth execution without errors")
        print("   - Highlight the step-by-step process")
        print("   - Demonstrate the final result")
        
        input("\n⏸️  Press Enter to start the demo...")
        
        start_time = time.time()
        session = await self.agent.run(query)
        execution_time = time.time() - start_time
        
        result = {
            "demo_id": 3,
            "title": "Success Case - Normal Operation",
            "query": query,
            "execution_time": execution_time,
            "steps_executed": self.agent.step_count,
            "retries_used": self.agent.retry_count,
            "human_interventions": 0,
            "success": session.state.get("original_goal_achieved", False),
            "timestamp": datetime.now().isoformat()
        }
        
        self.demo_results.append(result)
        print(f"\n✅ Demo 3 completed in {execution_time:.2f}s")
        print(f"   Steps: {result['steps_executed']}, Retries: {result['retries_used']}")
        
        return result

    async def demo_4_mixed_success_failure(self):
        """Demo 4: Mixed Success/Failure Scenario"""
        print("\n" + "="*80)
        print("🎬 YOUTUBE DEMO 4: Mixed Success/Failure Scenario")
        print("="*80)
        print("📝 Script: This demo shows both success and failure in the same query.")
        
        query = "Calculate 2 to the power of 8, then divide by zero, then add 5"
        print(f"\n🔍 Query: {query}")
        print("\n📋 Expected Behavior:")
        print("   1. Step 1: Power calculation succeeds (256)")
        print("   2. Step 2: Division by zero fails, triggers human intervention")
        print("   3. Human provides alternative: 'divide by 2 instead'")
        print("   4. Step 3: Add 5 to result (133)")
        print("   5. Query completes with human guidance")
        
        print("\n🎥 Recording Tips:")
        print("   - Show the successful first step")
        print("   - Demonstrate the failure and human intervention")
        print("   - Show how human guidance resolves the issue")
        print("   - Highlight the final successful completion")
        
        input("\n⏸️  Press Enter to start the demo...")
        
        start_time = time.time()
        session = await self.agent.run(query)
        execution_time = time.time() - start_time
        
        result = {
            "demo_id": 4,
            "title": "Mixed Success/Failure Scenario",
            "query": query,
            "execution_time": execution_time,
            "steps_executed": self.agent.step_count,
            "retries_used": self.agent.retry_count,
            "human_interventions": self.agent.retry_count,
            "success": session.state.get("original_goal_achieved", False),
            "timestamp": datetime.now().isoformat()
        }
        
        self.demo_results.append(result)
        print(f"\n✅ Demo 4 completed in {execution_time:.2f}s")
        print(f"   Steps: {result['steps_executed']}, Retries: {result['retries_used']}")
        
        return result

    async def demo_5_document_analysis_failure(self):
        """Demo 5: Document Analysis with Failures"""
        print("\n" + "="*80)
        print("🎬 YOUTUBE DEMO 5: Document Analysis with Failures")
        print("="*80)
        print("📝 Script: This demo shows document operations with failures.")
        
        query = "Search for Tesla documents, extract non-existent content, analyze the results"
        print(f"\n🔍 Query: {query}")
        print("\n📋 Expected Behavior:")
        print("   1. Step 1: Document search succeeds")
        print("   2. Step 2: Content extraction fails (non-existent content)")
        print("   3. Human intervention triggered")
        print("   4. Human provides alternative approach or manual result")
        print("   5. Step 3: Analysis proceeds with human guidance")
        
        print("\n🎥 Recording Tips:")
        print("   - Show document search success")
        print("   - Demonstrate extraction failure")
        print("   - Show human intervention options")
        print("   - Highlight recovery with human guidance")
        
        input("\n⏸️  Press Enter to start the demo...")
        
        start_time = time.time()
        session = await self.agent.run(query)
        execution_time = time.time() - start_time
        
        result = {
            "demo_id": 5,
            "title": "Document Analysis with Failures",
            "query": query,
            "execution_time": execution_time,
            "steps_executed": self.agent.step_count,
            "retries_used": self.agent.retry_count,
            "human_interventions": self.agent.retry_count,
            "success": session.state.get("original_goal_achieved", False),
            "timestamp": datetime.now().isoformat()
        }
        
        self.demo_results.append(result)
        print(f"\n✅ Demo 5 completed in {execution_time:.2f}s")
        print(f"   Steps: {result['steps_executed']}, Retries: {result['retries_used']}")
        
        return result

    async def demo_6_web_search_failure(self):
        """Demo 6: Web Search with Network Failures"""
        print("\n" + "="*80)
        print("🎬 YOUTUBE DEMO 6: Web Search with Network Failures")
        print("="*80)
        print("📝 Script: This demo shows web search operations with network issues.")
        
        query = "Search for latest AI news and calculate how many results were found"
        print(f"\n🔍 Query: {query}")
        print("\n📋 Expected Behavior:")
        print("   1. Step 1: Web search may fail due to network issues")
        print("   2. Human intervention triggered")
        print("   3. Human provides alternative: 'use cached results' or 'manual search'")
        print("   4. Step 2: Calculation proceeds with human guidance")
        
        print("\n🎥 Recording Tips:")
        print("   - Show network failure scenario")
        print("   - Demonstrate human intervention options")
        print("   - Show how human guidance provides workaround")
        print("   - Highlight the final result")
        
        input("\n⏸️  Press Enter to start the demo...")
        
        start_time = time.time()
        session = await self.agent.run(query)
        execution_time = time.time() - start_time
        
        result = {
            "demo_id": 6,
            "title": "Web Search with Network Failures",
            "query": query,
            "execution_time": execution_time,
            "steps_executed": self.agent.step_count,
            "retries_used": self.agent.retry_count,
            "human_interventions": self.agent.retry_count,
            "success": session.state.get("original_goal_achieved", False),
            "timestamp": datetime.now().isoformat()
        }
        
        self.demo_results.append(result)
        print(f"\n✅ Demo 6 completed in {execution_time:.2f}s")
        print(f"   Steps: {result['steps_executed']}, Retries: {result['retries_used']}")
        
        return result

    async def demo_7_mathematical_edge_cases(self):
        """Demo 7: Mathematical Edge Cases"""
        print("\n" + "="*80)
        print("🎬 YOUTUBE DEMO 7: Mathematical Edge Cases")
        print("="*80)
        print("📝 Script: This demo shows mathematical edge cases and human alternatives.")
        
        query = "Calculate the factorial of 0, then find the square root of the result, then divide by 0"
        print(f"\n🔍 Query: {query}")
        print("\n📋 Expected Behavior:")
        print("   1. Step 1: Factorial of 0 succeeds (1)")
        print("   2. Step 2: Square root of 1 succeeds (1)")
        print("   3. Step 3: Division by 0 fails")
        print("   4. Human intervention triggered")
        print("   5. Human provides alternative approach")
        
        print("\n🎥 Recording Tips:")
        print("   - Show mathematical edge cases")
        print("   - Demonstrate human intervention for math errors")
        print("   - Show how human provides mathematical alternatives")
        print("   - Highlight the educational value")
        
        input("\n⏸️  Press Enter to start the demo...")
        
        start_time = time.time()
        session = await self.agent.run(query)
        execution_time = time.time() - start_time
        
        result = {
            "demo_id": 7,
            "title": "Mathematical Edge Cases",
            "query": query,
            "execution_time": execution_time,
            "steps_executed": self.agent.step_count,
            "retries_used": self.agent.retry_count,
            "human_interventions": self.agent.retry_count,
            "success": session.state.get("original_goal_achieved", False),
            "timestamp": datetime.now().isoformat()
        }
        
        self.demo_results.append(result)
        print(f"\n✅ Demo 7 completed in {execution_time:.2f}s")
        print(f"   Steps: {result['steps_executed']}, Retries: {result['retries_used']}")
        
        return result

    async def demo_8_file_operations_failure(self):
        """Demo 8: File Operations with Permission Issues"""
        print("\n" + "="*80)
        print("🎬 YOUTUBE DEMO 8: File Operations with Permission Issues")
        print("="*80)
        print("📝 Script: This demo shows file operation failures and human solutions.")
        
        query = "Create a thumbnail from an image and save it to a protected directory"
        print(f"\n🔍 Query: {query}")
        print("\n📋 Expected Behavior:")
        print("   1. Step 1: Thumbnail creation may succeed")
        print("   2. Step 2: Save to protected directory fails")
        print("   3. Human intervention triggered")
        print("   4. Human provides alternative: 'save to user directory' or 'skip save'")
        
        print("\n🎥 Recording Tips:")
        print("   - Show file operation success")
        print("   - Demonstrate permission failure")
        print("   - Show human intervention options")
        print("   - Highlight the practical solution")
        
        input("\n⏸️  Press Enter to start the demo...")
        
        start_time = time.time()
        session = await self.agent.run(query)
        execution_time = time.time() - start_time
        
        result = {
            "demo_id": 8,
            "title": "File Operations with Permission Issues",
            "query": query,
            "execution_time": execution_time,
            "steps_executed": self.agent.step_count,
            "retries_used": self.agent.retry_count,
            "human_interventions": self.agent.retry_count,
            "success": session.state.get("original_goal_achieved", False),
            "timestamp": datetime.now().isoformat()
        }
        
        self.demo_results.append(result)
        print(f"\n✅ Demo 8 completed in {execution_time:.2f}s")
        print(f"   Steps: {result['steps_executed']}, Retries: {result['retries_used']}")
        
        return result

    async def demo_9_database_connection_failure(self):
        """Demo 9: Database Operations with Connection Issues"""
        print("\n" + "="*80)
        print("🎬 YOUTUBE DEMO 9: Database Operations with Connection Issues")
        print("="*80)
        print("📝 Script: This demo shows database connection failures and human workarounds.")
        
        query = "Connect to database, query user data, and calculate statistics"
        print(f"\n🔍 Query: {query}")
        print("\n📋 Expected Behavior:")
        print("   1. Step 1: Database connection may fail")
        print("   2. Human intervention triggered")
        print("   3. Human provides alternative: 'use mock data' or 'retry connection'")
        print("   4. Subsequent steps proceed with human guidance")
        
        print("\n🎥 Recording Tips:")
        print("   - Show database connection failure")
        print("   - Demonstrate human intervention options")
        print("   - Show how human provides workaround")
        print("   - Highlight the practical solution")
        
        input("\n⏸️  Press Enter to start the demo...")
        
        start_time = time.time()
        session = await self.agent.run(query)
        execution_time = time.time() - start_time
        
        result = {
            "demo_id": 9,
            "title": "Database Operations with Connection Issues",
            "query": query,
            "execution_time": execution_time,
            "steps_executed": self.agent.step_count,
            "retries_used": self.agent.retry_count,
            "human_interventions": self.agent.retry_count,
            "success": session.state.get("original_goal_achieved", False),
            "timestamp": datetime.now().isoformat()
        }
        
        self.demo_results.append(result)
        print(f"\n✅ Demo 9 completed in {execution_time:.2f}s")
        print(f"   Steps: {result['steps_executed']}, Retries: {result['retries_used']}")
        
        return result

    async def demo_10_api_rate_limiting(self):
        """Demo 10: API Operations with Rate Limiting"""
        print("\n" + "="*80)
        print("🎬 YOUTUBE DEMO 10: API Operations with Rate Limiting")
        print("="*80)
        print("📝 Script: This demo shows API rate limiting and human alternatives.")
        
        query = "Search for weather data, analyze results, and create summary"
        print(f"\n🔍 Query: {query}")
        print("\n📋 Expected Behavior:")
        print("   1. Step 1: API call may fail due to rate limiting")
        print("   2. Human intervention triggered")
        print("   3. Human provides alternative: 'use cached data' or 'wait and retry'")
        print("   4. Analysis proceeds with human guidance")
        
        print("\n🎥 Recording Tips:")
        print("   - Show API rate limiting failure")
        print("   - Demonstrate human intervention options")
        print("   - Show how human provides workaround")
        print("   - Highlight the practical solution")
        
        input("\n⏸️  Press Enter to start the demo...")
        
        start_time = time.time()
        session = await self.agent.run(query)
        execution_time = time.time() - start_time
        
        result = {
            "demo_id": 10,
            "title": "API Operations with Rate Limiting",
            "query": query,
            "execution_time": execution_time,
            "steps_executed": self.agent.step_count,
            "retries_used": self.agent.retry_count,
            "human_interventions": self.agent.retry_count,
            "success": session.state.get("original_goal_achieved", False),
            "timestamp": datetime.now().isoformat()
        }
        
        self.demo_results.append(result)
        print(f"\n✅ Demo 10 completed in {execution_time:.2f}s")
        print(f"   Steps: {result['steps_executed']}, Retries: {result['retries_used']}")
        
        return result

    async def run_all_demos(self):
        """Run all YouTube demos"""
        print("🎬 YOUTUBE DEMO SCRIPT - Human-in-the-Loop System")
        print("="*80)
        print("This script will run 10 different demos showing various aspects")
        print("of the human-in-the-loop system for YouTube recording.")
        
        await self.initialize_agent()
        
        # Run all demos
        await self.demo_1_tool_failure_division_by_zero()
        await self.demo_2_step_failure_max_steps()
        await self.demo_3_success_case()
        await self.demo_4_mixed_success_failure()
        await self.demo_5_document_analysis_failure()
        await self.demo_6_web_search_failure()
        await self.demo_7_mathematical_edge_cases()
        await self.demo_8_file_operations_failure()
        await self.demo_9_database_connection_failure()
        await self.demo_10_api_rate_limiting()
        
        # Generate demo summary
        self.generate_demo_summary()
    
    def generate_demo_summary(self):
        """Generate a summary of all demos"""
        print("\n" + "="*80)
        print("📊 YOUTUBE DEMO SUMMARY")
        print("="*80)
        
        total_demos = len(self.demo_results)
        successful_demos = sum(1 for r in self.demo_results if r['success'])
        total_steps = sum(r['steps_executed'] for r in self.demo_results)
        total_retries = sum(r['retries_used'] for r in self.demo_results)
        total_interventions = sum(r['human_interventions'] for r in self.demo_results)
        total_time = sum(r['execution_time'] for r in self.demo_results)
        
        print(f"Total Demos: {total_demos}")
        print(f"Successful Demos: {successful_demos}")
        print(f"Success Rate: {(successful_demos/total_demos)*100:.1f}%")
        print(f"Total Steps Executed: {total_steps}")
        print(f"Total Retries Used: {total_retries}")
        print(f"Total Human Interventions: {total_interventions}")
        print(f"Total Execution Time: {total_time:.2f}s")
        print(f"Average Demo Time: {total_time/total_demos:.2f}s")
        
        print(f"\n📋 Demo Breakdown:")
        for result in self.demo_results:
            status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
            print(f"  Demo {result['demo_id']}: {result['title']} - {status}")
            print(f"    Steps: {result['steps_executed']}, Retries: {result['retries_used']}, Time: {result['execution_time']:.2f}s")
        
        # Save results
        self.save_demo_results()
    
    def save_demo_results(self):
        """Save demo results to file"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"youtube_demo_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.demo_results, f, indent=2)
        
        print(f"\n💾 Demo results saved to: {filename}")

async def main():
    """Main function to run YouTube demos"""
    demo_scripts = YouTubeDemoScripts()
    await demo_scripts.run_all_demos()

if __name__ == "__main__":
    asyncio.run(main())
