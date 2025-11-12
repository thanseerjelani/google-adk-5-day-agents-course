# Day 2: Agent Tools & Advanced Patterns - Complete Reference

## 🎯 Overview

**Day 2 Focus**: Transform agents from isolated LLMs into capable systems that can interact with external services, execute code, and handle complex workflows requiring human oversight.

**Two Main Topics**:

1. **Task 2A**: Custom Tools & Code Execution
2. **Task 2B**: MCP Integration & Long-Running Operations

---

## 📦 New Components (Day 2)

### From Task 2A:

```python
from google.adk.agents import LlmAgent
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.tools import ToolContext, AgentTool
```

### From Task 2B:

```python
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.apps.app import App, ResumabilityConfig
from google.adk.runners import Runner
```

---

## 🔧 Task 2A: Custom Tools & Code Execution

### **Core Concept: Why Tools?**

**Without Tools**: Agent's knowledge is frozen in time, no real-world connection

**With Tools**: Agent can take actions and access live data

---

### **1. Custom Function Tools**

**What**: Turn any Python function into an agent tool

**Best Practices** (CRITICAL for reliability):

| Practice               | Why It Matters                   | Example                                     |
| ---------------------- | -------------------------------- | ------------------------------------------- |
| **Dictionary Returns** | Structured data + error handling | `{"status": "success", "data": ...}`        |
| **Clear Docstrings**   | LLM learns when/how to use tool  | Tool description in plain English           |
| **Type Hints**         | ADK generates proper schemas     | `def func(x: str) -> dict:`                 |
| **Error Handling**     | Graceful failure responses       | `{"status": "error", "error_message": ...}` |

**Pattern**:

```python
def get_exchange_rate(base: str, target: str) -> dict:
    """Gets currency exchange rate between two currencies.

    Args:
        base: Currency code to convert from (e.g., "USD")
        target: Currency code to convert to (e.g., "EUR")

    Returns:
        {"status": "success", "rate": 0.93} or
        {"status": "error", "error_message": "..."}
    """
    # Implementation with error handling
    rate = database.get(base, {}).get(target)
    if rate:
        return {"status": "success", "rate": rate}
    return {"status": "error", "error_message": f"Pair {base}/{target} not found"}
```

**Adding to Agent**:

```python
agent = LlmAgent(
    name="currency_agent",
    tools=[get_exchange_rate, get_fee_for_payment]  # Just add functions
)
```

---

### **2. Code Execution for Reliability**

**Problem**: LLMs are unreliable at math calculations

**Solution**: Generate Python code → Execute it → Use result

**Built-in Code Executor**:

```python
calculation_agent = LlmAgent(
    name="Calculator",
    code_executor=BuiltInCodeExecutor(),  # Enables code execution
    instruction="Generate ONLY Python code. No text. Must print result."
)
```

**How it works**:

1. Agent generates Python code (e.g., `print(500 * 0.98 * 0.93)`)
2. BuiltInCodeExecutor runs code in sandbox
3. Returns actual computed result (not LLM guess)

**Uses Gemini's Code Execution capability** under the hood

---

### **3. Agent as Tool (AgentTool)**

**What**: Use one agent as a tool for another agent (delegation pattern)

**When to use**: Specialist tasks (calculations, formatting, analysis)

**Pattern**:

```python
# Create specialist agent
calculator = LlmAgent(name="Calculator", code_executor=BuiltInCodeExecutor())

# Use it as a tool in main agent
main_agent = LlmAgent(
    name="MainAgent",
    tools=[
        get_rates,
        AgentTool(agent=calculator)  # Wrap specialist as tool
    ]
)
```

**Flow**:

```
User Query → Main Agent → Calls calculator (via AgentTool)
                       → Calculator generates code
                       → Code executes → Returns result
                       → Main Agent uses result → Response
```

---

### **Agent Tool vs Sub-Agent** (Important Distinction)

| Aspect       | Agent Tool                   | Sub-Agent                        |
| ------------ | ---------------------------- | -------------------------------- |
| **Control**  | Caller stays in control      | Control transfers completely     |
| **Return**   | Result goes back to caller   | New agent handles conversation   |
| **Use Case** | Delegation for specific task | Handoff to specialist            |
| **Example**  | "Calculate this for me"      | "Transfer to billing department" |

**Day 2 uses Agent Tools** (delegation, not handoff)

---

### **Complete Tool Types in ADK**

#### **Custom Tools** (You build them)

1. **Function Tools** ✅ _Used in Task 2A_

   - Any Python function
   - Example: `get_exchange_rate`, `get_fee`

2. **Long-Running Function Tools** ✅ _Used in Task 2B_

   - Operations requiring wait time
   - Example: Human approval, file processing

3. **Agent Tools** ✅ _Used in Task 2A_

   - Other agents as tools
   - Example: Calculator agent

4. **MCP Tools** ✅ _Used in Task 2B_

   - Connect to Model Context Protocol servers
   - Example: GitHub, Slack, Filesystem

5. **OpenAPI Tools**
   - Auto-generated from API specs
   - Example: REST API endpoints

#### **Built-in Tools** (Pre-made by ADK)

1. **Gemini Tools** ✅ _Used in Day 1 & 2_

   - `google_search`
   - `BuiltInCodeExecutor`

2. **Google Cloud Tools**

   - BigQuery, Spanner, API Hub
   - Requires Google Cloud access

3. **Third-party Tools**
   - Hugging Face, Firecrawl, GitHub

---

## 🌐 Task 2B: MCP & Long-Running Operations

### **1. Model Context Protocol (MCP)**

**What**: Open standard for connecting agents to external services

**Why**: No need to write custom API integrations - use community-built servers

**Architecture**:

```
Your Agent (MCP Client)
        ↓
    MCP Protocol (standardized)
        ↓
    ┌───────┬───────┬───────┐
    │GitHub │ Slack │ Maps  │  ← MCP Servers
    └───────┴───────┴───────┘
```

**Pattern**:

```python
# Step 1: Create MCP Toolset
mcp_server = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-everything"],
            tool_filter=["getTinyImage"]  # Only use specific tools
        ),
        timeout=30
    )
)

# Step 2: Add to agent
agent = LlmAgent(
    tools=[mcp_server]  # Agent can now use MCP tools
)
```

**What happens behind the scenes**:

1. ADK launches MCP server via `npx`
2. Establishes communication channel
3. Server announces available tools
4. Tools appear in agent's toolset automatically
5. Agent calls tool → ADK forwards to server → Returns result

**Popular MCP Servers**:

- **Everything Server**: Test/demo server (getTinyImage)
- **Kaggle MCP**: Dataset/notebook operations
- **GitHub MCP**: PR/issue analysis
- **Filesystem MCP**: File operations

---

### **2. Long-Running Operations (LRO)**

**What**: Tools that need to pause and wait for external input (usually human approval)

**When to use**:

- 💰 Financial transactions requiring approval
- 🗑️ Bulk operations (delete 1000 records)
- 📋 Compliance checkpoints
- 💸 High-cost actions (spin up 50 servers)
- ⚠️ Irreversible operations

**Key Components**:

| Component                    | Purpose                                |
| ---------------------------- | -------------------------------------- |
| **ToolContext**              | Provides pause/resume capabilities     |
| **request_confirmation()**   | Pauses execution, requests human input |
| **tool_confirmation**        | Contains human's decision after resume |
| **App + ResumabilityConfig** | Saves state for pause/resume           |
| **invocation_id**            | Tracks which execution to resume       |

---

### **LRO Pattern: Three Scenarios**

```python
def place_order(num_items: int, tool_context: ToolContext) -> dict:
    """Tool that pauses for approval on large orders."""

    # SCENARIO 1: Small order - auto-approve
    if num_items <= 5:
        return {"status": "approved", "order_id": "AUTO-123"}

    # SCENARIO 2: First call - PAUSE for approval
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"Large order: {num_items} items. Approve?",
            payload={"num_items": num_items}
        )
        return {"status": "pending"}  # Agent sees this

    # SCENARIO 3: Second call - RESUME with decision
    if tool_context.tool_confirmation.confirmed:
        return {"status": "approved", "order_id": "HUMAN-456"}
    else:
        return {"status": "rejected"}
```

---

### **LRO Setup Requirements**

**Step 1: Create Agent with LRO Tool**

```python
agent = LlmAgent(
    name="shipping_agent",
    tools=[FunctionTool(func=place_order)]
)
```

**Step 2: Wrap in Resumable App** (CRITICAL!)

```python
app = App(
    name="shipping_app",
    root_agent=agent,
    resumability_config=ResumabilityConfig(is_resumable=True)
)
```

**Why App?** Regular agent is stateless. App adds persistence to save/restore state.

**Step 3: Create Runner with App**

```python
runner = Runner(
    app=app,  # Pass app, not agent!
    session_service=InMemorySessionService()
)
```

---

### **LRO Workflow Pattern**

```python
async def run_workflow(query: str, approve: bool):
    # 1. Send initial request
    events = []
    async for event in runner.run_async(
        session_id="session_123",
        new_message=query_content
    ):
        events.append(event)

    # 2. Check if paused (look for special event)
    approval_info = check_for_approval(events)  # Returns invocation_id

    # 3. If paused, resume with human decision
    if approval_info:
        async for event in runner.run_async(
            session_id="session_123",
            new_message=approval_response,  # Human's decision
            invocation_id=approval_info["invocation_id"]  # CRITICAL: Same ID = resume
        ):
            # Process resumed execution
```

**Key: invocation_id ties pause and resume together**

---

### **LRO Event Flow Timeline**

```
TIME 1: User sends "Ship 10 containers"
TIME 2: runner.run_async() assigns invocation_id="abc123"
TIME 3: Agent calls place_order(10)
TIME 4: Tool sees num > 5, calls request_confirmation()
TIME 5: Tool returns {"status": "pending"}
TIME 6: ADK creates adk_request_confirmation event (invocation_id="abc123")
TIME 7: Workflow detects event, saves invocation_id
TIME 8: Get human decision → True
TIME 9: runner.run_async(invocation_id="abc123") ← RESUME
TIME 10: ADK loads saved state from TIME 6
TIME 11: Tool runs again, now with tool_confirmation.confirmed=True
TIME 12: Tool returns {"status": "approved"}
TIME 13: Agent responds to user
```

**Critical**: Same `invocation_id` tells ADK to **resume** (not restart)

---

## 🎓 Key Concepts Summary

### **ToolContext**

Object automatically provided to tools by ADK. Enables:

- `request_confirmation()`: Pause execution
- `tool_confirmation`: Check human's decision after resume

### **ResumabilityConfig**

Configuration that makes an App save/restore state for pause/resume workflows.

### **invocation_id**

Unique identifier for each `run_async()` call. Used to resume the correct paused execution.

### **adk_request_confirmation Event**

Special event ADK creates when a tool calls `request_confirmation()`. Your workflow must detect this to know the agent paused.

### **App vs Agent**

- **Agent**: Stateless, no memory between calls
- **App**: Wraps agent, adds persistence layer for resumability

---

## 🏗️ Architecture Patterns

### **Pattern 1: Multi-Tool Agent**

```
Agent with multiple function tools for specialized logic
├── Function Tool 1 (fees)
├── Function Tool 2 (rates)
└── Agent Tool (calculator)
```

### **Pattern 2: MCP Integration**

```
Agent → MCP Toolset → External MCP Server → Service (GitHub, Slack, etc.)
```

### **Pattern 3: Long-Running Operation**

```
App (resumable) → Agent → LRO Tool
                           ↓
                   request_confirmation()
                           ↓
                   Workflow detects pause
                           ↓
                   Get human decision
                           ↓
                   Resume with invocation_id
```

---

## 📊 Decision Matrix: When to Use What?

| Need                  | Solution           | Components                             |
| --------------------- | ------------------ | -------------------------------------- |
| Custom business logic | Function Tools     | Python function + type hints           |
| Reliable calculations | Code Execution     | BuiltInCodeExecutor                    |
| Specialist delegation | Agent Tools        | AgentTool(specialist_agent)            |
| External services     | MCP Tools          | McpToolset + MCP server                |
| Human approval        | Long-Running Tools | ToolContext + App + ResumabilityConfig |

---

## ⚠️ Common Pitfalls

### **Pitfall 1: Math in Instructions**

❌ Bad: "Calculate the final amount"
✅ Good: "Generate Python code to calculate, use calculator agent"

### **Pitfall 2: Missing Error Handling in Tools**

❌ Bad: `return exchange_rate`
✅ Good: `return {"status": "success", "rate": exchange_rate}`

### **Pitfall 3: Using Agent Instead of App for LRO**

❌ Bad: `Runner(agent=my_agent)`
✅ Good: `Runner(app=my_app)` where app has `resumability_config`

### **Pitfall 4: Forgetting invocation_id on Resume**

❌ Bad: `runner.run_async(new_message=approval)`
✅ Good: `runner.run_async(new_message=approval, invocation_id=saved_id)`

### **Pitfall 5: Not Checking tool_confirmation**

❌ Bad: Tool always assumes first call
✅ Good: `if not tool_context.tool_confirmation:` (first) vs else (resume)

---

## 🚀 Production Considerations

### **For Function Tools**:

- ✅ Always return status field for error checking
- ✅ Validate inputs before processing
- ✅ Use descriptive docstrings (LLM reads them!)
- ✅ Include examples in docstrings when complex

### **For MCP Integration**:

- ✅ Set appropriate timeouts
- ✅ Use tool_filter to limit exposed tools
- ✅ Test MCP server availability before deploying
- ✅ Handle connection failures gracefully

### **For Long-Running Operations**:

- ✅ Always wrap in App with resumability
- ✅ Save invocation_id reliably
- ✅ Set reasonable approval timeouts
- ✅ Handle "approval expired" scenarios
- ✅ Store approval decisions for audit trail

---

## 🎯 Real-World Use Cases

### **Function Tools**:

- Currency conversion with fee calculation
- Data validation and sanitization
- Business rule enforcement
- Custom calculations

### **Code Execution**:

- Financial calculations
- Data transformations
- Complex math/statistics
- Algorithm implementation

### **Agent Tools**:

- Format conversion (CSV → JSON)
- Text analysis/summarization
- Code generation
- Translation services

### **MCP Tools**:

- GitHub PR reviews
- Slack notifications
- Database queries
- File system operations
- Calendar management

### **Long-Running Tools**:

- Purchase approvals
- Bulk delete confirmations
- Contract signing workflows
- Admin privilege escalations
- Data export requests

---

## 📚 Quick Reference: Code Snippets

### **Function Tool Template**:

```python
def my_tool(param: str) -> dict:
    """Brief description of what tool does.

    Args:
        param: Description of parameter

    Returns:
        {"status": "success", "data": ...} or {"status": "error", ...}
    """
    try:
        result = do_something(param)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}
```

### **Agent Tool Usage**:

```python
specialist = LlmAgent(name="Specialist", ...)
main_agent = LlmAgent(tools=[AgentTool(agent=specialist)])
```

### **MCP Tool Setup**:

```python
mcp = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "mcp-server-package"],
            tool_filter=["tool1", "tool2"]
        )
    )
)
```

### **LRO Tool Template**:

```python
def lro_tool(items: int, tool_context: ToolContext) -> dict:
    if items <= THRESHOLD:
        return {"status": "approved"}

    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(hint="Approve?")
        return {"status": "pending"}

    if tool_context.tool_confirmation.confirmed:
        return {"status": "approved"}
    return {"status": "rejected"}
```

### **Resumable App Setup**:

```python
app = App(
    root_agent=agent,
    resumability_config=ResumabilityConfig(is_resumable=True)
)
runner = Runner(app=app, session_service=session_service)
```

---

## ✅ Day 2 Learning Outcomes

- ✅ Convert Python functions to agent tools (Function Tools)
- ✅ Implement reliable calculations via code execution
- ✅ Use agents as tools for delegation (Agent Tools)
- ✅ Connect to external services via MCP
- ✅ Implement human-in-the-loop workflows (LRO)
- ✅ Build resumable applications with state persistence
- ✅ Understand all ADK tool types and when to use each

---

## 🔗 Resources

- **ADK Tools Documentation**: https://developers.google.com/adk/tools
- **MCP Servers**: https://modelcontextprotocol.io/examples
- **Code Execution**: Gemini's built-in capability
- **Kaggle MCP**: https://www.kaggle.com/mcp

---

## 🎯 Next: Day 3 Preview

**Topics**: Sessions, State Management, Multi-turn Conversations

- Manual session creation and management
- State persistence across conversations
- Context management
- Advanced orchestration patterns
