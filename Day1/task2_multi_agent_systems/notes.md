# Task 2: Multi-Agent Systems - Notes

## 🎯 Goal

Learn to build specialized agent teams that collaborate using different orchestration patterns.

---

## 🏗️ Four Orchestration Patterns

### 1. LLM-Based Orchestration (Dynamic)

**What**: Root agent with LLM brain decides which sub-agents to call

**Structure**:

```
User → Root Agent → [Sub-Agent 1, Sub-Agent 2, ...] → Response
```

**When to use**:

- ✅ Need flexible, adaptive workflows
- ✅ Different queries need different agent combinations
- ✅ Want dynamic decision-making

**Pros**: Flexible, adapts to situations
**Cons**: Unpredictable, might skip steps

**Example**: Research coordinator that decides whether to research or summarize

---

### 2. Sequential Workflow (Assembly Line)

**What**: Agents run in fixed order, output flows to next agent

**Structure**:

```
User → Agent 1 → Agent 2 → Agent 3 → Response
```

**When to use**:

- ✅ Order matters
- ✅ Each step builds on previous
- ✅ Need predictable execution

**Pros**: Reliable, easy to debug
**Cons**: Slow, can't parallelize

**Example**: Blog creation (Outline → Write → Edit)

---

### 3. Parallel Workflow (Concurrent)

**What**: Multiple agents run simultaneously, results combined later

**Structure**:

```
         ┌→ Agent 1 →┐
User → Parallel┼→ Agent 2 →┼→ Aggregator → Response
         └→ Agent 3 →┘
```

**When to use**:

- ✅ Tasks are independent
- ✅ Speed is important
- ✅ No dependencies between tasks

**Pros**: Fast (3x speed for 3 agents), efficient
**Cons**: Uses more API quota, needs resources

**Example**: Multi-topic research (Tech || Health || Finance)

---

### 4. Loop Workflow (Iterative Refinement)

**What**: Agents repeat in cycle until work is approved

**Structure**:

```
User → Initial → Loop[Critic → Refiner] → Final
                  ↑________________|
                 (repeats until approved)
```

**When to use**:

- ✅ Need quality improvement
- ✅ Review and refinement required
- ✅ Iterative process needed

**Pros**: Quality through iteration, self-correcting
**Cons**: Slower, uses more calls

**Example**: Story writing with critic feedback

---

## 🔑 Key Concepts Deep Dive

### output_key

**Purpose**: Names where agent stores results in session state

```python
agent = Agent(
    output_key="research_findings"  # Saves result here
)
```

**Analogy**: Like a variable name in programming

---

### {placeholders}

**Purpose**: Injects data from session state into agent instructions

```python
agent = Agent(
    instruction="Summarize this: {research_findings}"  # Gets data here
)
```

**Analogy**: Like using variables in a template

---

### Session State

**Purpose**: Shared memory where agents store and retrieve data

**Evolution Example** (Blog Pipeline):

```python
# After OutlineAgent
state = {"blog_outline": "..."}

# After WriterAgent
state = {"blog_outline": "...", "blog_draft": "..."}

# After EditorAgent
state = {"blog_outline": "...", "blog_draft": "...", "final_blog": "..."}
```

---

### AgentTool

**Purpose**: Wraps an agent so other agents can call it

```python
research_agent = Agent(...)
root = Agent(
    tools=[AgentTool(research_agent)]  # Now callable as a tool
)
```

**Analogy**: Turning a specialist into a consultant that others can hire

---

### FunctionTool

**Purpose**: Wraps Python functions so agents can call them

```python
def exit_loop():
    return {"status": "done"}

agent = Agent(
    tools=[FunctionTool(exit_loop)]  # Function now callable
)
```

**Analogy**: Giving agents a button to press for special actions

---

## 💡 Design Principles Learned

### 1. Single Responsibility

Each agent should have **one clear job**

❌ **Bad**: Agent that researches, writes, edits, and formats
✅ **Good**: Four separate agents, each doing one thing well

### 2. Clear Data Flow

Use descriptive names for output_key and placeholders

❌ **Bad**: `output_key="data"`, `{result}`
✅ **Good**: `output_key="research_findings"`, `{research_findings}`

### 3. Pattern Selection

Choose the right pattern for the job:

- Order matters? → Sequential
- Independent tasks? → Parallel
- Need refinement? → Loop
- Need flexibility? → LLM-based

### 4. Safety First

Always set `max_iterations` in loops

```python
loop = LoopAgent(
    sub_agents=[...],
    max_iterations=3  # Prevents infinite loops
)
```

---

## 🎓 Pattern Comparison

| Pattern    | Order        | Speed    | Use Case           | API Calls      |
| ---------- | ------------ | -------- | ------------------ | -------------- |
| LLM-based  | Dynamic      | Medium   | Flexible workflows | Variable       |
| Sequential | Fixed        | Slow     | Step-by-step       | N agents       |
| Parallel   | Simultaneous | Fast     | Independent tasks  | N at once      |
| Loop       | Repeated     | Variable | Refinement         | N × iterations |

---

## 🐛 Challenges & Solutions

### Challenge 1: API Quota Exhausted (429 Error)

**Problem**: Parallel workflow used too many simultaneous calls
**Solution**:

- Switched to different API key
- Added delays between test runs
- Reduced number of parallel agents

# Task 2: Multi-Agent Systems - Notes

## 🎯 Goal

Learn to build specialized agent teams that collaborate using different orchestration patterns.

---

## 🏗️ Four Orchestration Patterns

### 1. LLM-Based Orchestration (Dynamic)

**What**: Root agent with LLM brain decides which sub-agents to call

**Structure**:

```
User → Root Agent → [Sub-Agent 1, Sub-Agent 2, ...] → Response
```

**When to use**:

- ✅ Need flexible, adaptive workflows
- ✅ Different queries need different agent combinations
- ✅ Want dynamic decision-making

**Pros**: Flexible, adapts to situations
**Cons**: Unpredictable, might skip steps

**Example**: Research coordinator that decides whether to research or summarize

---

### 2. Sequential Workflow (Assembly Line)

**What**: Agents run in fixed order, output flows to next agent

**Structure**:

```
User → Agent 1 → Agent 2 → Agent 3 → Response
```

**When to use**:

- ✅ Order matters
- ✅ Each step builds on previous
- ✅ Need predictable execution

**Pros**: Reliable, easy to debug
**Cons**: Slow, can't parallelize

**Example**: Blog creation (Outline → Write → Edit)

---

### 3. Parallel Workflow (Concurrent)

**What**: Multiple agents run simultaneously, results combined later

**Structure**:

```
         ┌→ Agent 1 →┐
User → Parallel┼→ Agent 2 →┼→ Aggregator → Response
         └→ Agent 3 →┘
```

**When to use**:

- ✅ Tasks are independent
- ✅ Speed is important
- ✅ No dependencies between tasks

**Pros**: Fast (3x speed for 3 agents), efficient
**Cons**: Uses more API quota, needs resources

**Example**: Multi-topic research (Tech || Health || Finance)

---

### 4. Loop Workflow (Iterative Refinement)

**What**: Agents repeat in cycle until work is approved

**Structure**:

```
User → Initial → Loop[Critic → Refiner] → Final
                  ↑________________|
                 (repeats until approved)
```

**When to use**:

- ✅ Need quality improvement
- ✅ Review and refinement required
- ✅ Iterative process needed

**Pros**: Quality through iteration, self-correcting
**Cons**: Slower, uses more calls

**Example**: Story writing with critic feedback

---

## 🔑 Key Concepts Deep Dive

### output_key

**Purpose**: Names where agent stores results in session state

```python
agent = Agent(
    output_key="research_findings"  # Saves result here
)
```

**Analogy**: Like a variable name in programming

---

### {placeholders}

**Purpose**: Injects data from session state into agent instructions

```python
agent = Agent(
    instruction="Summarize this: {research_findings}"  # Gets data here
)
```

**Analogy**: Like using variables in a template

---

### Session State

**Purpose**: Shared memory where agents store and retrieve data

**Evolution Example** (Blog Pipeline):

```python
# After OutlineAgent
state = {"blog_outline": "..."}

# After WriterAgent
state = {"blog_outline": "...", "blog_draft": "..."}

# After EditorAgent
state = {"blog_outline": "...", "blog_draft": "...", "final_blog": "..."}
```

---

### AgentTool

**Purpose**: Wraps an agent so other agents can call it

```python
research_agent = Agent(...)
root = Agent(
    tools=[AgentTool(research_agent)]  # Now callable as a tool
)
```

**Analogy**: Turning a specialist into a consultant that others can hire

---

### FunctionTool

**Purpose**: Wraps Python functions so agents can call them

```python
def exit_loop():
    return {"status": "done"}

agent = Agent(
    tools=[FunctionTool(exit_loop)]  # Function now callable
)
```

**Analogy**: Giving agents a button to press for special actions

---

## 💡 Design Principles Learned

### 1. Single Responsibility

Each agent should have **one clear job**

❌ **Bad**: Agent that researches, writes, edits, and formats
✅ **Good**: Four separate agents, each doing one thing well

### 2. Clear Data Flow

Use descriptive names for output_key and placeholders

❌ **Bad**: `output_key="data"`, `{result}`
✅ **Good**: `output_key="research_findings"`, `{research_findings}`

### 3. Pattern Selection

Choose the right pattern for the job:

- Order matters? → Sequential
- Independent tasks? → Parallel
- Need refinement? → Loop
- Need flexibility? → LLM-based

### 4. Safety First

Always set `max_iterations` in loops

```python
loop = LoopAgent(
    sub_agents=[...],
    max_iterations=3  # Prevents infinite loops
)
```

---

## 🎓 Pattern Comparison

| Pattern    | Order        | Speed    | Use Case           | API Calls      |
| ---------- | ------------ | -------- | ------------------ | -------------- |
| LLM-based  | Dynamic      | Medium   | Flexible workflows | Variable       |
| Sequential | Fixed        | Slow     | Step-by-step       | N agents       |
| Parallel   | Simultaneous | Fast     | Independent tasks  | N at once      |
| Loop       | Repeated     | Variable | Refinement         | N × iterations |

---

## 🐛 Challenges & Solutions

### Challenge 1: API Quota Exhausted (429 Error)

**Problem**: Parallel workflow used too many simultaneous calls
**Solution**:

- Switched to different API key
- Added delays between test runs
- Reduced number of parallel agents

### Challenge 2: Understanding State Flow

**Problem**: Confused about how data passes between agents
**Solution**:

- Drew state diagrams on paper
- Realized output_key = write, {placeholder} = read
- State is like a shared whiteboard
