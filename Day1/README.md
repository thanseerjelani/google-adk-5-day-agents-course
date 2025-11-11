# Day 1: Introduction to AI Agents

## 🎯 Learning Objectives

- Understand difference between LLM and AI Agent
- Build first agent with tools
- Learn multi-agent orchestration patterns

## 📋 Tasks Completed

### Task 1: First AI Agent

**Goal**: Build an agent that can use Google Search tool

**What I Built**:

- Simple agent with google_search capability
- Learned about Agent, Runner, and Tool components

**Code**: [first_agent.py](./task1_first_agent/first_agent.py)

**Key Code Snippet**:

```python
root_agent = Agent(
    name="helpful_assistant",
    model="gemini-2.5-flash-lite",
    instruction="Use Google Search for current info",
    tools=[google_search],
)
```

**Output Screenshot**:
![Agent Response](./task1_first_agent/screenshots/output.png)

---

### Task 2: Multi-Agent Systems

**Goal**: Learn orchestration patterns

**What I Built**:

1. **LLM-Orchestrated System**: Research + Summarization
2. **Sequential Workflow**: Blog creation pipeline
3. **Parallel Workflow**: Multi-topic research
4. **Loop Workflow**: Story refinement with critic

**Code Files**:

- [llm_orchestration.py](./task2_multi_agent_systems/llm_orchestration.py)
- [sequential_workflow.py](./task2_multi_agent_systems/sequential_workflow.py)
- [parallel_workflow.py](./task2_multi_agent_systems/parallel_workflow.py)
- [loop_workflow.py](./task2_multi_agent_systems/loop_workflow.py)

---

## 💡 Key Learnings

### Concepts Mastered

- `output_key`: Storing agent results in session state
- `{placeholders}`: Injecting state data into agent instructions
- `AgentTool`: Wrapping agents as callable tools
- `FunctionTool`: Wrapping Python functions as tools

### When to Use Each Pattern

| Pattern    | Use Case                       |
| ---------- | ------------------------------ |
| Sequential | Order matters, linear pipeline |
| Parallel   | Independent tasks, need speed  |
| Loop       | Iterative improvement needed   |
| LLM-based  | Dynamic decision-making        |

---

## 🐛 Challenges & Solutions

### Challenge 1: API Quota Exhausted

**Problem**: Got 429 error when running parallel agents
**Solution**: Used different API key, added delays between requests

### Challenge 2: Understanding State Flow

**Problem**: Confused about how data passes between agents
**Solution**: Realized `output_key` stores data, `{placeholder}` retrieves it

---

## 🎓 Resources

- [Day 1 Reference Guide](../resources/reference_guides/day1_reference.md)
- [Kaggle Notebook](https://www.kaggle.com/thanseer2001)
- [ADK Documentation](https://developers.google.com/adk)

---

## 📊 Stats

- **Time Spent**: ~3 hours
- **Code Written**: ~200 lines
- **Agents Built**: 12
- **API Calls Made**: ~50

## ⏭️ Next Steps

Moving to Day 2 to learn about [next topic]
