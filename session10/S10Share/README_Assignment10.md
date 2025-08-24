# Assignment 10: Enhanced Multi-Agent System

This implementation adds advanced features to the multi-agent system including human-in-the-loop capabilities, performance monitoring, and robust error handling.

## 🚀 New Features

### 1. Human-in-the-Loop for Tool Failures
When a tool fails, the system now prompts for human intervention with options:
- Suggest alternative approach
- Provide manual result
- Skip the step
- Retry with different parameters

### 2. Human-in-the-Loop for Plan Failures
When a plan fails (reaches max steps), the system prompts for human guidance:
- Provide new plan steps
- Modify existing plan
- Provide direct answer
- Start over with different approach

### 3. Max Steps and Retries Enforcement
- **Max Steps = 3**: Limits the number of steps per session
- **Max Retries = 3**: Limits retry attempts for failed tools
- Automatic enforcement with human intervention when limits are reached

### 4. Tool Performance Logging
- Tracks success/failure rates for each tool
- Records execution times and error messages
- Maintains reliability scores for tool selection
- Saves performance data to `tool_performance_log.json`

### 5. Comprehensive Testing Simulator
- Runs 100+ tests with sleep functionality to avoid rate limiting
- Tests various query types and failure scenarios
- Generates detailed performance reports
- Saves results to timestamped JSON files

## 📁 File Structure

```
S10Share/
├── agent/
│   └── agent_loop2.py          # Enhanced agent with Assignment 10 features
├── simulator.py                 # 100+ test simulator
├── test_features.py            # Feature testing script
├── tool_performance_log.json   # Tool performance data (auto-generated)
├── simulation_results_*.json   # Test results (auto-generated)
└── feature_test_results_*.json # Feature test results (auto-generated)
```

## 🛠️ Usage

### Running the Enhanced Agent
```bash
python main.py
```

### Running Feature Tests
```bash
python test_features.py
```

### Running the Simulator (100+ Tests)
```bash
python simulator.py
```

## 🔧 Configuration

### Max Steps and Retries
Edit `agent/agent_loop2.py`:
```python
MAX_STEPS = 3      # Maximum steps per session
MAX_RETRIES = 3    # Maximum retries per tool failure
```

### Simulator Settings
Edit `simulator.py`:
```python
await simulator.run_simulation(
    num_tests=100,              # Number of tests to run
    sleep_between_tests=2.0     # Sleep time between tests (seconds)
)
```

## 📊 Monitoring and Logging

### Tool Performance Log
The system automatically logs tool performance to `tool_performance_log.json`:
```json
{
  "add": {
    "total_calls": 15,
    "successful_calls": 14,
    "failed_calls": 1,
    "avg_execution_time": 0.023,
    "last_errors": ["Invalid input"]
  }
}
```

### Reliability Scoring
Tools are scored based on their success rate:
- 0.0 = 0% success rate
- 1.0 = 100% success rate
- Unknown tools default to 0.5

## 🧪 Testing Features

### Automated Tests
The `test_features.py` script tests:
- ✅ Max steps enforcement
- ✅ Max retries enforcement  
- ✅ Tool performance logging
- ✅ Tool reliability scoring
- ⚠️ Human-in-the-loop (requires manual testing)

### Manual Testing
To test human-in-the-loop features:

1. **Tool Failure Testing**:
   ```bash
   python main.py
   # Enter: "Divide by zero"
   # Follow prompts when tool fails
   ```

2. **Plan Failure Testing**:
   ```bash
   python main.py
   # Enter a complex query that will take more than 3 steps
   # Follow prompts when max steps are reached
   ```

## 📈 Performance Metrics

The simulator tracks:
- **Success Rate**: Percentage of successful queries
- **Average Execution Time**: Mean time per query
- **Step Analysis**: Average steps per test
- **Retry Analysis**: Average retries per test
- **Tool Performance**: Success rates for each tool

## 🔍 Debugging

### Viewing Tool Performance
```python
# In agent_loop2.py
print(f"Tool reliability: {self.get_tool_reliability_score('tool_name')}")
print(f"Tool performance log: {self.tool_performance_log}")
```

### Session Tracing
The agent provides detailed session traces:
```
=== LIVE AGENT SESSION TRACE ===
Session ID: uuid
Query: user query
Max Steps: 3, Max Retries: 3
Step Count: 1/3
```

## 🚨 Error Handling

### Tool Failures
1. Automatic retry (up to MAX_RETRIES)
2. Human-in-the-loop intervention
3. Performance logging
4. Tool switching based on reliability scores

### Plan Failures
1. Max steps enforcement
2. Human-in-the-loop plan guidance
3. Plan modification or restart
4. Direct answer provision

## 📋 Assignment 10 Checklist

- ✅ If a tool fails, add "Human-In-Loop" and let him answer that part
- ✅ If a plan fails, then add "Human-In-Loop" and suggest a plan, and show the Agent listens
- ✅ Enforce Max_Steps = 3, and Max_Retries = 3
- ✅ Write a simulator that runs 100+ Tests. Please add "sleep," or else Google will ban you
- ✅ Save a tool_performance log, and feed it to Agent (for this, you need to run multiple tools multiple times)

## 🔄 Future Enhancements

1. **Adaptive Limits**: Dynamic max steps/retries based on query complexity
2. **Learning from Human Interventions**: Improve future decisions based on human guidance
3. **Advanced Tool Selection**: Use reliability scores to choose most reliable tools
4. **Performance Optimization**: Cache successful tool combinations
5. **Real-time Monitoring**: Web dashboard for live performance monitoring

## 📝 Notes

- The simulator includes sleep functionality to prevent rate limiting
- Tool performance data persists between sessions
- Human-in-the-loop features require manual testing
- All features are backward compatible with existing code
- Performance logs are automatically saved and loaded

## 🎯 Key Benefits

1. **Robustness**: Human intervention prevents complete failures
2. **Learning**: Tool performance tracking improves future decisions
3. **Scalability**: Simulator enables large-scale testing
4. **Debugging**: Comprehensive logging and monitoring
5. **User Experience**: Clear feedback and guidance during failures
