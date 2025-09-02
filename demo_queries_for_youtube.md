# YouTube Demo Queries for Human-in-the-Loop System

## Demo 1: Tool Failure with Human Intervention

### Query for Tool Failure Demo:
```
"Divide 10 by 0 and then calculate the square root of -1"
```

**Expected Behavior:**
- The `divide` tool will fail with "division by zero" error
- The `sqrt` tool will fail with "math domain error" 
- System will trigger human-in-the-loop intervention
- User will be prompted with 4 options:
  1. Suggest alternative approach
  2. Provide manual result  
  3. Skip this step
  4. Retry with different parameters

### Alternative Tool Failure Queries:
```
"Access a non-existent file and call an undefined function"
"Calculate factorial of -5 and divide by zero"
"Create thumbnail from invalid image path"
"Convert invalid string to integers"
```

## Demo 2: Step Failure with Human Intervention

### Query for Step Failure Demo:
```
"Calculate the factorial of 10, then find its square root, then multiply by 5, then add 100, then divide by 2, then find the cube root, then calculate sine of the result"
```

**Expected Behavior:**
- This query requires more than 3 steps (MAX_STEPS = 3)
- System will reach max steps limit
- Human-in-the-loop will be triggered for plan failure
- User will be prompted with 4 options:
  1. Provide new plan steps
  2. Modify existing plan
  3. Provide direct answer
  4. Start over with different approach

### Alternative Step Failure Queries:
```
"Search for Tesla documents, extract key points, analyze content, summarize findings, create report, format output, save to file"
"Calculate fibonacci of 20, find sum, multiply by 2, add 100, divide by 3, find square root, calculate factorial"
"Find AI news, analyze sentiment, extract keywords, create summary, format as JSON, save to database, send notification"
```

## Demo 3: Complex Multi-Step Query (Success Case)

### Query for Success Demo:
```
"Calculate 5 factorial and then add 10 to the result"
```

**Expected Behavior:**
- Step 1: Calculate factorial of 5 (120)
- Step 2: Add 10 to result (130)
- Query completes successfully within 3 steps
- No human intervention required

## Demo 4: Mixed Success/Failure Scenario

### Query for Mixed Demo:
```
"Calculate 2 to the power of 8, then divide by zero, then add 5"
```

**Expected Behavior:**
- Step 1: Power calculation succeeds (256)
- Step 2: Division by zero fails, triggers human intervention
- Human provides alternative: "divide by 2 instead"
- Step 3: Add 5 to result (133)
- Query completes with human guidance

## Demo 5: Document Analysis with Failures

### Query for Document Demo:
```
"Search for Tesla documents, extract non-existent content, analyze the results"
```

**Expected Behavior:**
- Step 1: Document search succeeds
- Step 2: Content extraction fails (non-existent content)
- Human intervention triggered
- Human provides alternative approach or manual result
- Step 3: Analysis proceeds with human guidance

## Demo 6: Web Search with Network Failures

### Query for Web Demo:
```
"Search for latest AI news and calculate how many results were found"
```

**Expected Behavior:**
- Step 1: Web search may fail due to network issues
- Human intervention triggered
- Human provides alternative: "use cached results" or "manual search"
- Step 2: Calculation proceeds with human guidance

## Demo 7: Mathematical Operations with Edge Cases

### Query for Math Demo:
```
"Calculate the factorial of 0, then find the square root of the result, then divide by 0"
```

**Expected Behavior:**
- Step 1: Factorial of 0 succeeds (1)
- Step 2: Square root of 1 succeeds (1)
- Step 3: Division by 0 fails
- Human intervention triggered
- Human provides alternative approach

## Demo 8: File Operations with Permission Issues

### Query for File Demo:
```
"Create a thumbnail from an image and save it to a protected directory"
```

**Expected Behavior:**
- Step 1: Thumbnail creation may succeed
- Step 2: Save to protected directory fails
- Human intervention triggered
- Human provides alternative: "save to user directory" or "skip save"

## Demo 9: Database Operations with Connection Issues

### Query for Database Demo:
```
"Connect to database, query user data, and calculate statistics"
```

**Expected Behavior:**
- Step 1: Database connection may fail
- Human intervention triggered
- Human provides alternative: "use mock data" or "retry connection"
- Subsequent steps proceed with human guidance

## Demo 10: API Operations with Rate Limiting

### Query for API Demo:
```
"Search for weather data, analyze results, and create summary"
```

**Expected Behavior:**
- Step 1: API call may fail due to rate limiting
- Human intervention triggered
- Human provides alternative: "use cached data" or "wait and retry"
- Analysis proceeds with human guidance

## Human Intervention Response Examples

### For Tool Failures:
1. **Alternative Approach**: "Use a different mathematical method"
2. **Manual Result**: "The result is 42"
3. **Skip Step**: "Skip this calculation"
4. **Retry with Parameters**: "Try with different input values"

### For Step Failures:
1. **New Plan**: "Focus on the first 2 calculations only"
2. **Modify Plan**: "Combine steps 2 and 3"
3. **Direct Answer**: "The final answer is 150"
4. **Different Approach**: "Use a simpler calculation method"

## YouTube Recording Tips

1. **Tool Failure Demo**: Show the error message, then demonstrate each of the 4 human intervention options
2. **Step Failure Demo**: Show the step counter reaching 3, then demonstrate plan failure intervention
3. **Success Demo**: Show smooth execution without human intervention
4. **Mixed Demo**: Show both success and failure in the same query
5. **Document Demo**: Show document search success followed by extraction failure
6. **Web Demo**: Show network failure and human guidance
7. **Math Demo**: Show mathematical edge cases and human alternatives
8. **File Demo**: Show file operation failures and human solutions
9. **Database Demo**: Show connection issues and human workarounds
10. **API Demo**: Show rate limiting and human alternatives

## Expected Human Responses for Demos

### Tool Failure Responses:
- "Use 1 instead of 0 for division"
- "The square root of -1 is i (imaginary number)"
- "Skip the division step"
- "Try dividing by 2 instead"

### Step Failure Responses:
- "Just calculate factorial of 5 and add 10"
- "Combine the multiplication and addition into one step"
- "The answer is 130"
- "Use a calculator approach instead"

## Demo Script Flow

1. **Introduction**: Explain the human-in-the-loop system
2. **Tool Failure Demo**: Show tool failure and 4 intervention options
3. **Step Failure Demo**: Show step limit and plan failure intervention
4. **Success Demo**: Show normal operation without intervention
5. **Statistics**: Show tool performance and success rates
6. **Conclusion**: Summarize the benefits of human-in-the-loop system
