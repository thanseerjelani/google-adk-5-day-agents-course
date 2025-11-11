# Day 1: Multi-Agent Systems - Complete Reference Guide

## 🎯 Core Concept: Why Multi-Agent Systems?

### **The Problem: Monolithic "Do-It-All" Agents**

A single agent trying to do everything (research, write, edit, fact-check) becomes:

- ❌ Complex and hard to maintain
- ❌ Difficult to debug (which part failed?)
- ❌ Long, confusing instruction prompts
- ❌ Unreliable results
- ❌ Can't reuse components

### **The Solution: Specialized Agent Teams**

Multiple simple agents, each with **one clear job**, working together:

- ✅ Easier to build and test
- ✅ Clear responsibilities
- ✅ Reusable components
- ✅ More reliable and predictable
- ✅ Easier to debug and improve

**Real-World Analogy**: Instead of one person doing research, writing, editing, and publishing, you have a **team** where each person specializes in one area.

---

## 📦 New ADK Components (Day 2)

### **1. SequentialAgent**

```python
from google.adk.agents import SequentialAgent
```

**What it does**: Runs sub-agents in a **fixed, predictable order** (like an assembly line).

**Purpose**: Guarantees step-by-step execution where each agent's output becomes the next agent's input.

**When to use**:

- Order matters
- Linear pipeline needed
- Each step builds on the previous one

**Key Feature**: **Deterministic** - always runs in the same order.

---

### **2. ParallelAgent**

```python
from google.adk.agents import ParallelAgent
```

**What it does**: Runs multiple sub-agents **simultaneously** (at the same time).

**Purpose**: Speeds up workflows by executing independent tasks concurrently.

**When to use**:

- Tasks are independent (don't need each other's results)
- Speed is important
- Can execute concurrently

**Key Feature**: **Concurrent execution** - dramatically faster than sequential.

---

### **3. LoopAgent**

```python
from google.adk.agents import LoopAgent
```

**What it does**: Runs sub-agents **repeatedly** until a condition is met or max iterations reached.

**Purpose**: Creates refinement cycles for iterative improvement.

**When to use**:

- Iterative improvement needed
- Quality refinement matters
- Review and revise cycles required

**Key Feature**: **Iterative refinement** - keeps improving until "good enough".

---

### **4. AgentTool**

```python
from google.adk.tools import AgentTool
```

**What it does**: Wraps an agent so it can be used as a **tool** by another agent.

**Purpose**: Makes agents callable by other agents, enabling agent-to-agent communication.

**How it works**: Converts an agent into a tool that appears in another agent's tool list.

**Example**:

```python
research_agent = Agent(name="ResearchAgent", ...)
root_agent = Agent(
    name="Coordinator",
    tools=[AgentTool(research_agent)]  # research_agent is now a tool
)
```

---

### **5. FunctionTool**

```python
from google.adk.tools import FunctionTool
```

**What it does**: Wraps a **Python function** so it can be used as a tool by an agent.

**Purpose**: Allows agents to call custom Python functions for specific operations.

**How it works**: Converts any Python function into a tool that agents can invoke.

**Example**:

```python
def exit_loop():
    """Signals the loop to stop"""
    return {"status": "approved"}

agent = Agent(
    name="RefinerAgent",
    tools=[FunctionTool(exit_loop)]  # Function is now a tool
)
```

---

## 🔑 Key Concepts Explained Simply

### **output_key**

**What it is**: A label/name for storing an agent's result in the session state.

**Purpose**: Allows agents to share data with each other.

**How it works**:

```python
agent = Agent(
    name="WriterAgent",
    output_key="blog_draft"  # Stores result as "blog_draft"
)
```

**Think of it as**: A variable name where the agent saves its output.

---

### **State Placeholders**

**What they are**: Variables in `{curly braces}` in agent instructions.

**Purpose**: Inject data from session state into agent prompts.

**How it works**:

```python
agent = Agent(
    instruction="Edit this draft: {blog_draft}"  # Gets "blog_draft" from state
)
```

**The magic**: Automatically replaced with actual content when agent runs.

---

### **Session State**

**What it is**: A temporary storage area that holds data during a conversation.

**Purpose**: Allows agents to pass information to each other.

**How it works**:

1. Agent A runs and stores result with `output_key="data"`
2. Session state now contains `{"data": "result from Agent A"}`
3. Agent B uses `{data}` in its instruction to access that result

**Think of it as**: A shared whiteboard where agents write and read information.

---

### **Sub-agents**

**What they are**: Agents that are managed/coordinated by a parent agent.

**Purpose**: The worker agents in a multi-agent system.

**Example**:

```python
# These are sub-agents
outline_agent = Agent(...)
writer_agent = Agent(...)

# This parent agent manages them
root = SequentialAgent(
    sub_agents=[outline_agent, writer_agent]  # Sub-agents listed here
)
```

---

### **Root Agent (Coordinator)**

**What it is**: The top-level agent that orchestrates the entire workflow.

**Purpose**: Acts as the "manager" that coordinates all sub-agents.

**Think of it as**: The project manager who delegates tasks to team members.

---

## 🏗️ Multi-Agent Architecture Patterns

### **Pattern 1: LLM-Based Orchestration (Dynamic)**

**How it works**: A root agent with an LLM "brain" decides which sub-agents to call and in what order.

**Architecture**:

```
User → Root Agent (LLM decides) → [Sub-Agent 1, Sub-Agent 2, ...] → Response
```

**Code Breakdown**:

```python
# Step 1: Create specialized sub-agents
research_agent = Agent(
    name="ResearchAgent",
    instruction="Use google_search to find information",
    tools=[google_search],
    output_key="research_findings"  # Saves result here
)

summarizer_agent = Agent(
    name="SummarizerAgent",
    instruction="Create summary from: {research_findings}",  # Uses data from research_agent
    output_key="final_summary"
)

# Step 2: Wrap sub-agents as tools
root_agent = Agent(
    name="Coordinator",
    instruction="""
    1. First, call ResearchAgent to find info
    2. Then, call SummarizerAgent to summarize
    3. Present the summary
    """,
    tools=[
        AgentTool(research_agent),      # Makes research_agent callable
        AgentTool(summarizer_agent)     # Makes summarizer_agent callable
    ]
)

# Step 3: Run the system
runner = InMemoryRunner(agent=root_agent)
response = await runner.run_debug("Your query")
```

**Pros**:

- Flexible - LLM can adapt to different situations
- Dynamic decision-making

**Cons**:

- Unpredictable - LLM might skip steps or change order
- Harder to debug

---

### **Pattern 2: Sequential Workflow (Assembly Line)**

**How it works**: Agents run in a **fixed order**, one after another. Output flows from one to the next.

**Architecture**:

```
User → Agent 1 → Agent 2 → Agent 3 → Response
```

**Code Breakdown**:

```python
# Step 1: Create agents that build on each other
outline_agent = Agent(
    name="OutlineAgent",
    instruction="Create a blog outline",
    output_key="blog_outline"  # First output
)

writer_agent = Agent(
    name="WriterAgent",
    instruction="Write a post following: {blog_outline}",  # Uses outline
    output_key="blog_draft"  # Second output
)

editor_agent = Agent(
    name="EditorAgent",
    instruction="Edit this draft: {blog_draft}",  # Uses draft
    output_key="final_blog"  # Final output
)

# Step 2: Chain them in a SequentialAgent
root_agent = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[
        outline_agent,   # Runs first
        writer_agent,    # Runs second (gets outline)
        editor_agent     # Runs third (gets draft)
    ]
)

# Step 3: Run the pipeline
runner = InMemoryRunner(agent=root_agent)
response = await runner.run_debug("Write about AI agents")
```

**How data flows**:

1. `outline_agent` creates outline → stores in `blog_outline`
2. `writer_agent` reads `{blog_outline}` → writes draft → stores in `blog_draft`
3. `editor_agent` reads `{blog_draft}` → edits → stores in `final_blog`

**Pros**:

- Predictable and reliable
- Easy to debug (know exact order)
- Each step builds on previous

**Cons**:

- Slow (must wait for each step)
- Can't parallelize independent tasks

---

### **Pattern 3: Parallel Workflow (Concurrent Tasks)**

**How it works**: Multiple agents run **at the same time**, then results are combined.

**Architecture**:

```
               ┌→ Agent 1 →┐
User → Parallel┼→ Agent 2 →┼→ Aggregator → Response
               └→ Agent 3 →┘
```

**Code Breakdown**:

```python
# Step 1: Create independent research agents
tech_researcher = Agent(
    name="TechResearcher",
    instruction="Research AI/ML trends",
    tools=[google_search],
    output_key="tech_research"  # Each has own output_key
)

health_researcher = Agent(
    name="HealthResearcher",
    instruction="Research medical breakthroughs",
    tools=[google_search],
    output_key="health_research"
)

finance_researcher = Agent(
    name="FinanceResearcher",
    instruction="Research fintech trends",
    tools=[google_search],
    output_key="finance_research"
)

# Step 2: Create aggregator to combine results
aggregator_agent = Agent(
    name="Aggregator",
    instruction="""
    Combine these findings:
    Tech: {tech_research}
    Health: {health_research}
    Finance: {finance_research}

    Create executive summary highlighting themes.
    """,
    output_key="executive_summary"
)

# Step 3: Nest Parallel inside Sequential
parallel_team = ParallelAgent(
    name="ResearchTeam",
    sub_agents=[
        tech_researcher,      # All three run
        health_researcher,    # at the same
        finance_researcher    # time
    ]
)

root_agent = SequentialAgent(
    name="ResearchSystem",
    sub_agents=[
        parallel_team,        # Runs first (all 3 parallel)
        aggregator_agent      # Runs second (after all 3 done)
    ]
)

# Step 4: Run the system
runner = InMemoryRunner(agent=root_agent)
response = await runner.run_debug("Executive briefing")
```

**How it works**:

1. All 3 researchers start **simultaneously**
2. Each completes independently (no waiting)
3. Once **all 3 are done**, aggregator combines results

**Pros**:

- **Fast** - 3x faster than sequential for 3 agents
- Efficient use of resources
- Great for independent tasks

**Cons**:

- Uses more API quota (multiple simultaneous calls)
- Can't use if tasks depend on each other

---

### **Pattern 4: Loop Workflow (Iterative Refinement)**

**How it works**: Agents run repeatedly in a cycle until work is "good enough" or max iterations reached.

**Architecture**:

```
User → Initial Agent → Loop[Critic → Refiner] → Final Output
                        ↑________________|
                      (repeats until approved)
```

**Code Breakdown**:

```python
# Step 1: Create initial draft agent (runs once)
initial_writer = Agent(
    name="InitialWriter",
    instruction="Write first draft of story",
    output_key="current_story"  # Creates first version
)

# Step 2: Create critic agent (reviews work)
critic_agent = Agent(
    name="Critic",
    instruction="""
    Review story: {current_story}

    If well-written, respond: "APPROVED"
    Otherwise, give 2-3 specific suggestions
    """,
    output_key="critique"  # Stores feedback
)

# Step 3: Create exit function
def exit_loop():
    """Signals loop to stop"""
    return {"status": "approved", "message": "Story approved"}

# Step 4: Create refiner agent (improves or exits)
refiner_agent = Agent(
    name="Refiner",
    instruction="""
    Story: {current_story}
    Critique: {critique}

    IF critique is "APPROVED", call exit_loop function
    OTHERWISE, rewrite story based on feedback
    """,
    output_key="current_story",  # Overwrites with improved version
    tools=[FunctionTool(exit_loop)]  # Can call exit function
)

# Step 5: Create loop structure
refinement_loop = LoopAgent(
    name="RefinementLoop",
    sub_agents=[
        critic_agent,    # Runs first in loop
        refiner_agent    # Runs second in loop
    ],
    max_iterations=2  # Safety limit (prevents infinite loops)
)

# Step 6: Wrap in sequential workflow
root_agent = SequentialAgent(
    name="StoryPipeline",
    sub_agents=[
        initial_writer,     # Runs once at start
        refinement_loop     # Loops until approved or max_iterations
    ]
)

# Step 7: Run the system
runner = InMemoryRunner(agent=root_agent)
response = await runner.run_debug("Write story about lighthouse")
```

**How it works**:

1. `initial_writer` creates first draft → stores in `current_story`
2. **Loop starts**:
   - `critic_agent` reviews `{current_story}` → gives feedback in `critique`
   - `refiner_agent` reads both `{current_story}` and `{critique}`
   - If approved: calls `exit_loop()` → loop stops
   - If not approved: rewrites story → overwrites `current_story`
3. **Loop repeats** until approved or `max_iterations` reached

**Key Insight**: `refiner_agent` overwrites `current_story` each iteration, so critic sees the improved version next time!

**Pros**:

- Quality refinement through iteration
- Self-improving system
- Catches and fixes issues

**Cons**:

- Uses more API calls (each iteration = 2 calls)
- Must set `max_iterations` to prevent infinite loops
- Slower than single-pass systems

---

## 🔄 Understanding State Flow

### **Example: Blog Pipeline State Changes**

```python
# Initial State (empty)
state = {}

# After OutlineAgent runs
state = {
    "blog_outline": "1. Intro\n2. Main Points\n3. Conclusion"
}

# After WriterAgent runs (reads blog_outline, creates blog_draft)
state = {
    "blog_outline": "1. Intro\n2. Main Points\n3. Conclusion",
    "blog_draft": "Here is the full blog post based on outline..."
}

# After EditorAgent runs (reads blog_draft, creates final_blog)
state = {
    "blog_outline": "1. Intro\n2. Main Points\n3. Conclusion",
    "blog_draft": "Here is the full blog post based on outline...",
    "final_blog": "Here is the polished, edited version..."
}
```

**Key Point**: Each agent **adds** to state (except Loop which **overwrites**).

---

## 🎓 Pattern Comparison Table

| Pattern        | Execution Order | Speed    | Predictability | Best For               | API Calls          |
| -------------- | --------------- | -------- | -------------- | ---------------------- | ------------------ |
| **LLM-based**  | Dynamic         | Medium   | Low            | Flexible workflows     | Variable           |
| **Sequential** | Fixed order     | Slow     | High           | Step-by-step pipelines | N agents           |
| **Parallel**   | Simultaneous    | Fast     | High           | Independent tasks      | N agents (at once) |
| **Loop**       | Repeated cycles | Variable | High           | Iterative refinement   | N × iterations     |

---

## 🧩 Design Principles

### **1. Single Responsibility**

Each agent should have **one clear job**.

❌ Bad: Agent that researches, writes, and edits
✅ Good: Three agents - one researches, one writes, one edits

### **2. Clear Data Flow**

Use `output_key` and `{placeholders}` to make data flow explicit.

```python
agent1 = Agent(output_key="step1_result")
agent2 = Agent(instruction="Use {step1_result} to...")
```

### **3. Appropriate Pattern Selection**

- Tasks in order? → Sequential
- Tasks independent? → Parallel
- Need refinement? → Loop
- Need flexibility? → LLM-based

### **4. Error Handling**

Always set `max_iterations` in loops to prevent infinite execution:

```python
loop = LoopAgent(
    sub_agents=[...],
    max_iterations=3  # Safety net
)
```

---

## 💡 Common Patterns & Best Practices

### **Nested Workflows**

Combine patterns for complex systems:

```python
# Parallel research + Sequential processing
parallel = ParallelAgent(sub_agents=[r1, r2, r3])
sequential = SequentialAgent(
    sub_agents=[parallel, aggregator]
)
```

### **State Management**

Use descriptive `output_key` names:

```python
# ❌ Bad
output_key="result"

# ✅ Good
output_key="research_findings"
output_key="edited_draft"
output_key="final_summary"
```

### **Instruction Clarity**

Be explicit about what agents should do:

```python
# ❌ Bad
instruction="Process the data"

# ✅ Good
instruction="""
Your task is to:
1. Read the research findings: {research_findings}
2. Extract 3-5 key points
3. Format as bulleted list
"""
```

---

## 🐛 Debugging Multi-Agent Systems

### **How to Debug**

1. **Check State Flow**: Print `output_key` values
2. **Test Agents Individually**: Run each agent alone first
3. **Verify Placeholders**: Ensure `{placeholder}` names match `output_key`
4. **Watch Execution Order**: Sequential should run in order, Parallel simultaneously
5. **Monitor Loop Iterations**: Check if loop exits correctly

### **Common Issues**

| Problem               | Cause                                  | Solution                         |
| --------------------- | -------------------------------------- | -------------------------------- |
| Agent gets empty data | Wrong placeholder name                 | Match `{name}` to `output_key`   |
| Loop never stops      | No exit condition                      | Add `exit_loop()` function       |
| Slow execution        | Using Sequential for independent tasks | Switch to Parallel               |
| Quota exhausted       | Too many parallel calls                | Reduce parallelism or add delays |

---

## 🎯 When to Use Each Pattern

### **Use Sequential When:**

- ✅ Output of one agent is input for next
- ✅ Order is critical (outline → write → edit)
- ✅ Need predictable, reproducible results
- ✅ Debugging is important

### **Use Parallel When:**

- ✅ Tasks are completely independent
- ✅ Speed is priority
- ✅ No data dependencies between agents
- ✅ Have sufficient API quota

### **Use Loop When:**

- ✅ Need quality improvement cycles
- ✅ Review and refinement required
- ✅ Want self-correcting behavior
- ✅ Can define "good enough" criteria

### **Use LLM-based When:**

- ✅ Need dynamic decision-making
- ✅ Workflow varies by input
- ✅ Want flexible orchestration
- ✅ Tasks aren't strictly sequential

---

## 📊 Real-World Examples

### **Content Creation Pipeline (Sequential)**

```
Outline Agent → Writer Agent → Editor Agent → SEO Agent → Publisher Agent
```

### **Market Research System (Parallel)**

```
Competitor Analysis || Customer Feedback || Industry Trends
                        ↓
                  Market Report Agent
```

### **Code Review System (Loop)**

```
Initial Code → Loop[Code Reviewer → Code Refiner] → Final Code
```

### **Customer Support (LLM-based)**

```
Root Agent decides → [FAQ Agent | Technical Support | Escalation Agent]
```

---

## 🚀 Advanced Concepts

### **Hybrid Workflows**

Combine multiple patterns:

```python
# Research (Parallel) → Analysis (Sequential) → Refinement (Loop)
research_parallel = ParallelAgent(...)
analysis_sequential = SequentialAgent(...)
refinement_loop = LoopAgent(...)

root = SequentialAgent(
    sub_agents=[
        research_parallel,
        analysis_sequential,
        refinement_loop
    ]
)
```

### **Conditional Execution**

Use LLM-based orchestration for if/else logic:

```python
root = Agent(
    instruction="""
    IF query is about products, call ProductAgent
    ELSE IF query is about support, call SupportAgent
    ELSE call GeneralAgent
    """,
    tools=[
        AgentTool(product_agent),
        AgentTool(support_agent),
        AgentTool(general_agent)
    ]
)
```

---

## ✅ Day 2 Learning Outcomes

By completing Day 2, you now understand:

- ✅ Why multi-agent systems are better than monolithic agents
- ✅ Four workflow patterns and when to use each
- ✅ How to use `output_key` and placeholders for state management
- ✅ How to wrap agents and functions as tools
- ✅ How to design agent teams with clear responsibilities
- ✅ How to debug multi-agent workflows
- ✅ How to nest patterns for complex systems

---

## 🔗 Key Takeaways

1. **Specialization > Generalization**: Simple, focused agents work better than complex ones
2. **Pattern Selection Matters**: Choose Sequential/Parallel/Loop based on task requirements
3. **State is Everything**: Master `output_key` and `{placeholders}` for agent communication
4. **Predictability vs Flexibility**: Sequential/Parallel/Loop are predictable; LLM-based is flexible
5. **Safety First**: Always use `max_iterations` in loops
6. **Test Incrementally**: Build and test one agent at a time before combining

---

## 📚 Quick Reference: Components Summary

| Component         | Type         | Purpose                  | Example                |
| ----------------- | ------------ | ------------------------ | ---------------------- |
| `Agent`           | Base         | Single specialized agent | `Agent(name="Writer")` |
| `SequentialAgent` | Orchestrator | Fixed-order execution    | Pipeline workflows     |
| `ParallelAgent`   | Orchestrator | Concurrent execution     | Independent research   |
| `LoopAgent`       | Orchestrator | Iterative refinement     | Review/improve cycles  |
| `AgentTool`       | Wrapper      | Makes agents callable    | `AgentTool(agent)`     |
| `FunctionTool`    | Wrapper      | Makes functions callable | `FunctionTool(func)`   |
| `output_key`      | Property     | Names agent output       | State storage key      |
| `{placeholder}`   | Syntax       | Injects state data       | Accesses stored values |

---

## 🎯 Next: Day 3 Preview

Day 3 will cover **Sessions and State Management** - deep dive into how to manage conversation history, persist data, and handle complex multi-turn interactions.

**Key Topics**:

- Manual session creation
- Session persistence
- State manipulation
- Multi-turn conversations
- Context management

Get ready to level up your agent orchestration skills! 🚀
