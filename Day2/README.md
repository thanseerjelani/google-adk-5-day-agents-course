# Day 2: Agent Tools & Advanced Patterns

![Status](https://img.shields.io/badge/status-completed-success.svg)
![Tasks](https://img.shields.io/badge/tasks-2%2F2-blue.svg)

## 🎯 Learning Objectives

- ✅ Build custom function tools with best practices
- ✅ Implement code execution for reliable calculations
- ✅ Use agents as tools (delegation pattern)
- ✅ Connect to external services via MCP
- ✅ Build resumable workflows with human-in-the-loop
- ✅ Understand all ADK tool types

---

## 📋 Tasks Completed

### ✅ Task 2A: Custom Tools & Code Execution

**Duration**: ~3 hours  
**Goal**: Transform Python functions into agent tools and improve reliability

**What I Built**:

1. **Currency Converter** with custom function tools

   - Fee lookup tool
   - Exchange rate tool
   - Structured error handling

2. **Enhanced Currency Converter** with code execution
   - Calculator agent with BuiltInCodeExecutor
   - Agent-as-tool pattern (AgentTool)
   - Reliable math via code generation

**Files**:

- [currency_converter.py](./task2a_custom_tools/currency_converter.py)
- [code_execution_agent.py](./task2a_custom_tools/code_execution_agent.py)
- [enhanced_currency_agent.py](./task2a_custom_tools/enhanced_currency_agent.py)
- [notes.md](./task2a_custom_tools/notes.md)

**Key Learning**: Code execution is more reliable than LLM math!

---

### ✅ Task 2B: MCP & Long-Running Operations

**Duration**: ~3 hours  
**Goal**: Connect to external services and build pausable workflows

**What I Built**:

1. **MCP Integration** with Everything Server

   - Connected to external MCP server
   - Used getTinyImage tool
   - Displayed generated image

2. **Shipping Agent** with human approval
   - Tool that pauses for large orders (>5 containers)
   - Resumable workflow with state persistence
   - Approval/rejection handling

**Files**:

- [mcp_integration.py](./task2b_advanced_patterns/mcp_integration.py)
- [long_running_operations.py](./task2b_advanced_patterns/long_running_operations.py)
- [workflow_helpers.py](./task2b_advanced_patterns/workflow_helpers.py)
- [notes.md](./task2b_advanced_patterns/notes.md)

**Key Learning**: App + ResumabilityConfig enables pause/resume!

---

## 🔑 Core Concepts Mastered

### Function Tools Best Practices

```python
def tool(param: str) -> dict:
    """Clear docstring that LLM reads"""
    return {"status": "success", "data": result}
```

### Agent as Tool

```python
AgentTool(agent=specialist_agent)  # Delegate to specialist
```

### MCP Integration

```python
McpToolset(connection_params=StdioConnectionParams(...))
```

### Long-Running Operations

```python
tool_context.request_confirmation()  # Pause here
tool_context.tool_confirmation.confirmed  # Check decision
```

---

## 💡 Key Insights

### Tool Design

1. **Dictionary Returns**: Always include "status" field
2. **Type Hints**: Enable ADK to generate schemas
3. **Docstrings**: LLM reads them to understand tool usage
4. **Error Handling**: Structured error responses

### Reliability

- **Code Execution > LLM Math**: Generate Python code for calculations
- **Agent Tools**: Delegate specialized tasks to focused agents
- **MCP**: Reuse community-built integrations

### Long-Running Operations

- **ToolContext**: Enables pause/resume capabilities
- **App + Resumability**: Saves state across pauses
- **invocation_id**: Ties pause and resume together
- **Workflow Pattern**: Detect pause → Get decision → Resume

---

## 🐛 Challenges & Solutions

### Challenge 1: LLM Math Errors

**Problem**: Agent calculated 500 _ 0.98 _ 0.93 incorrectly  
**Solution**: Used BuiltInCodeExecutor to generate and run Python code  
**Learning**: Always use code execution for arithmetic

### Challenge 2: Understanding LRO Flow

**Problem**: Confused about when tool runs first vs second time  
**Solution**: Drew timeline diagram showing pause/resume sequence  
**Learning**: `tool_confirmation` is None on first call, populated on resume

### Challenge 3: MCP Server Connection

**Problem**: Initial timeout connecting to MCP server  
**Solution**: Increased timeout to 30 seconds, verified npx command  
**Learning**: MCP servers need time to launch and handshake

---

## 📊 Statistics

- **Tools Created**: 5 (2 function, 1 code executor, 1 MCP, 1 LRO)
- **Agents Built**: 4 (currency, calculator, image, shipping)
- **Patterns Learned**: 4 (function tools, agent tools, MCP, LRO)
- **Time Spent**: ~6 hours
- **API Calls**: ~40

---

## 🎓 Skills Acquired

### Technical

- ✅ Create custom function tools
- ✅ Implement code execution for reliability
- ✅ Use agents as tools (AgentTool pattern)
- ✅ Connect to MCP servers
- ✅ Build pausable workflows
- ✅ Handle approval events
- ✅ Resume execution with invocation_id

### Architectural

- ✅ Design tool APIs with status returns
- ✅ Structure error handling
- ✅ Choose appropriate tool types
- ✅ Build resumable applications
- ✅ Manage state across pauses

---

## 🚀 Real-World Applications

### What I Can Build Now

1. **Financial Systems**

   - Currency conversion with fees
   - Purchase approval workflows
   - Transaction compliance checks

2. **External Integrations**

   - GitHub PR analysis via MCP
   - Kaggle dataset operations
   - Slack notifications

3. **Human-in-the-Loop Processes**
   - Bulk operation approvals
   - High-cost action confirmations
   - Compliance checkpoints

---

### ✅ Exercise: Image Generation with Cost Approval

Built an AI agent that:

- Auto-approves single image requests
- Requires approval for bulk generation (>1 images)
- Calculates cost estimates ($0.02/image)
- Uses MCP for actual image generation

**File**: [image_generation_with_approval.py](./exercise/image_generation_with_approval.py)

**Key Achievement**: Successfully combined MCP integration with
long-running operations for cost-conscious AI system.

## 📚 Resources

- [Day 2 Reference Guide](../resources/reference_guides/day2_reference.md)
- [ADK Tools Documentation](https://developers.google.com/adk/tools)
- [MCP Servers](https://modelcontextprotocol.io/examples)
- [Kaggle Notebooks](https://www.kaggle.com/code/thanseer2001)
- [Day 2 Exercise](https://www.kaggle.com/code/thanseer2001/image-generation-agent-with-cost-approval)

---

## ⏭️ Next Steps

Ready for Day 3: Sessions & State Management!

---

**Day 2 Status**: ✅ **COMPLETE**  
**Last Updated**: [Current Date]
