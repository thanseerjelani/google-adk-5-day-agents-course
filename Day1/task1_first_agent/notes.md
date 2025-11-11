# Task 1: First AI Agent - Notes

## 🎯 Goal

Build a simple AI agent that can use external tools (Google Search) to answer questions requiring current information.

---

## 🔑 Key Concepts Learned

### 1. **LLM vs Agent**

- **LLM**: Just responds with text based on training data
  - `Prompt → LLM → Text Response`
- **Agent**: Can think, take actions, and use tools
  - `Prompt → Agent → Thought → Action → Observation → Final Answer`

### 2. **Core Components**

#### Agent

```python
Agent(
    name="helpful_assistant",
    model="gemini-2.5-flash-lite",
    description="Brief description",
    instruction="How the agent should behave",
    tools=[google_search]
)
```

- **name**: Identifier for the agent
- **model**: The LLM that powers reasoning
- **instruction**: The agent's "personality" and guidelines
- **tools**: External capabilities the agent can use

#### Runner

```python
InMemoryRunner(agent=root_agent)
```

- Orchestrates the conversation
- Manages execution of the agent
- Handles session creation (automatically in debug mode)

#### Tools

```python
from google.adk.tools import google_search
```

- External capabilities agents can use
- `google_search` allows web searching for current info

---

## 💡 How It Works

### Agent Decision Process:

1. **Receives Query**: User asks a question
2. **Analyzes Need**: Does it need current info?
3. **Tool Selection**: Decides to use google_search
4. **Tool Execution**: Searches the web
5. **Observation**: Receives search results
6. **Response**: Formulates answer using search data

### Example Flow:

```
User: "What's the weather in London?"
  ↓
Agent thinks: "I need current weather data"
  ↓
Agent uses: google_search tool
  ↓
Tool returns: Current weather information
  ↓
Agent responds: "The weather in London is currently 56°F and cloudy..."
```

---

## 🎓 What I Learned

### Technical Skills:

- ✅ How to configure an AI agent with ADK
- ✅ How to give agents tool capabilities
- ✅ How runners execute agents
- ✅ Difference between LLM and Agent behavior

### Key Insights:

1. **Tools extend capabilities**: Without google_search, agent can only use training data
2. **Instructions matter**: Clear instructions guide agent behavior
3. **Async execution**: Agent operations are asynchronous
4. **Debug mode**: `run_debug()` simplifies prototyping

---

## 🐛 Challenges Faced

### Challenge 1: API Key Setup

- **Issue**: Initially forgot to set API key in Kaggle Secrets
- **Solution**: Added GOOGLE_API_KEY to Kaggle Secrets with checkbox enabled

### Challenge 2: Understanding Async

- **Issue**: Confused about `await` keyword
- **Solution**: Realized agent operations are async, need to use `await` or `asyncio.run()`

---

## 🔧 Code Explanation

### Why these imports?

```python
from google.adk.agents import Agent          # Main agent class
from google.adk.runners import InMemoryRunner  # Executes agents
from google.adk.tools import google_search     # Web search capability
```

### Why InMemoryRunner?

- Stores session data in memory (temporary)
- Good for development and prototyping
- Automatically handles session creation with `run_debug()`

### Why gemini-2.5-flash-lite?

- Fast and efficient model
- Cost-effective
- Good balance of performance and speed
- Suitable for agent applications

---

## 📊 Test Results

### Query 1: "What is Agent Development Kit?"

- ✅ Agent used google_search
- ✅ Found current documentation
- ✅ Provided accurate answer with available languages (Python, Go, Java)

### Query 2: "What's the weather in London?"

- ✅ Agent searched for current weather
- ✅ Returned temperature, conditions, and forecast
- ✅ Response was up-to-date

### Query 3: Custom query testing

- ✅ Agent correctly identified when to search
- ✅ Didn't search for questions it already knew
- ✅ Provided relevant, current information

---

## 🚀 Next Steps

- [x] Built first agent with tools
- [x] Understood agent vs LLM difference
- [ ] Move to Task 2: Multi-agent systems
- [ ] Learn orchestration patterns

---

## 📚 Resources Referenced

- ADK Documentation: https://developers.google.com/adk
- Google AI Studio: https://aistudio.google.com/
- Kaggle Course Notebook: [Link to my notebook]
