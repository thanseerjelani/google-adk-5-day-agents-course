# Day 1: AI Agents with ADK - Complete Reference Guide

## 🎯 Core Concepts

### **LLM (Large Language Model)**

A trained AI model that generates text responses based on input prompts. It cannot take actions or access external information beyond its training data.

**Example Flow**: `Prompt → LLM → Text Response`

### **AI Agent**

An intelligent system that can reason, take actions, use tools, and observe results to accomplish tasks. Goes beyond simple text generation.

**Example Flow**: `Prompt → Agent → Thought → Action → Observation → Final Answer`

### **Agentic Behavior**

The ability of an AI system to autonomously make decisions, use tools, and take actions to achieve goals rather than just responding to prompts.

---

## 🛠️ ADK (Agent Development Kit)

### **What is ADK?**

A flexible, modular framework from Google for developing and deploying AI agents. Makes agent development similar to traditional software development.

**Key Features**:

- Optimized for Gemini models
- Model-agnostic (works with other LLMs)
- Deployment-agnostic (flexible hosting)
- Available in Python, Go, and Java

---

## 📦 Core ADK Components

### **1. Agent**

```python
from google.adk.agents import Agent
```

The main entity that represents your AI agent. Defines what the agent can do, how it behaves, and what tools it has access to.

**Key Properties**:

- `name`: Identifier for the agent
- `model`: The LLM powering the agent (e.g., "gemini-2.5-flash-lite")
- `description`: Brief explanation of the agent's purpose
- `instruction`: Guiding prompt that defines the agent's behavior and goals
- `tools`: List of capabilities the agent can use

**Purpose**: Encapsulates all configuration and behavior of your AI agent in one object.

---

### **2. Runner**

```python
from google.adk.runners import InMemoryRunner
```

The orchestrator that manages conversations, sends messages to agents, and handles responses. Acts as the execution engine for your agent.

**Types**:

- `InMemoryRunner`: Stores session data in memory (good for prototyping)
- Other runners available for production use

**Key Methods**:

- `run_debug()`: Quick prototyping method that abstracts session management
- Handles session creation and maintenance automatically

**Purpose**: Manages the entire conversation lifecycle and coordinates agent execution.

---

### **3. Tools**

```python
from google.adk.tools import google_search
```

External capabilities that agents can use to perform actions beyond text generation. Tools extend what an agent can do.

**Common Tools**:

- `google_search`: Allows agent to search the web for current information
- Custom tools can be created for specific needs

**How Tools Work**:

1. Agent inspects available tools
2. Agent decides when to use a tool based on instructions
3. Tool executes and returns results
4. Agent uses results to formulate response

**Purpose**: Give agents the ability to interact with external systems and retrieve real-time data.

---

### **4. Types**

```python
from google.genai import types
```

Data structures and type definitions for working with the Generative AI library. Ensures type safety and proper data formatting.

**Purpose**: Provides standard formats for requests, responses, and configurations.

---

## 🔑 Authentication & Setup

### **Gemini API Key**

Authentication credential required to use Google's Gemini models through the API.

**Where to Get**: [Google AI Studio](https://aistudio.google.com/app/apikey)

**Setup in Kaggle**:

1. Store in Kaggle Secrets as `GOOGLE_API_KEY`
2. Access via `UserSecretsClient().get_secret("GOOGLE_API_KEY")`
3. Set as environment variable `os.environ["GOOGLE_API_KEY"]`

---

## 🏗️ Agent Architecture

### **Agent Configuration Pattern**

```python
agent = Agent(
    name="helpful_assistant",
    model="gemini-2.5-flash-lite",
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info.",
    tools=[google_search]
)
```

### **Execution Pattern**

```python
runner = InMemoryRunner(agent=root_agent)
response = await runner.run_debug("Your question here")
```

---

## 🔄 Agent Workflow

### **Step-by-Step Process**:

1. **User Input**: Question or prompt is received
2. **Agent Reasoning**: Agent analyzes the request
3. **Tool Selection**: Agent decides if tools are needed
4. **Tool Execution**: Selected tool performs action (e.g., web search)
5. **Observation**: Agent receives tool results
6. **Response Generation**: Agent formulates final answer using all available information

**Example**:

- **Input**: "What's the weather in London?"
- **Thought**: "I need current weather data"
- **Action**: Use google_search tool
- **Observation**: Receives weather data from search
- **Output**: "The weather in London is currently 56°F and cloudy..."

---

## 🖥️ ADK Interfaces

### **Python Runner (Notebook)**

Direct Python API for running agents programmatically. Best for development and testing.

**Usage**: `runner.run_debug("prompt")`

### **ADK CLI Commands**

#### `adk create`

Creates a new agent project with folder structure, configuration files, and boilerplate code.

**Example**: `adk create sample-agent --model gemini-2.5-flash-lite --api_key $GOOGLE_API_KEY`

**Generated Files**:

- `agent.py`: Your agent code
- `.env`: Environment variables (API keys)
- `__init__.py`: Python package initialization

#### `adk web`

Launches interactive web interface for chatting with and debugging agents visually.

**Usage**: `adk web --url_prefix {url_prefix}`

**Features**:

- Visual chat interface
- Debug traces showing agent's thought process
- Real-time tool execution monitoring

#### `adk run`

Runs an agent from command line without web interface.

#### `adk api_server`

Starts an API server for production deployment of your agent.

---

## 🔍 Sessions

### **What is a Session?**

A conversation context that maintains state across multiple interactions with an agent. Keeps track of conversation history.

**In Day 1**: Automatically managed by `run_debug()` method for simplicity.

**Note**: Day 3 covers manual session creation and management in detail.

---

## 🎓 Key Differences

### **LLM vs Agent**

| Feature         | LLM                      | Agent                   |
| --------------- | ------------------------ | ----------------------- |
| **Capability**  | Text generation only     | Can take actions        |
| **Tools**       | None                     | Can use external tools  |
| **Information** | Limited to training data | Can access current info |
| **Process**     | One-shot response        | Multi-step reasoning    |

### **Prompt Engineering vs Agent Instructions**

| Aspect          | Prompt Engineering  | Agent Instructions               |
| --------------- | ------------------- | -------------------------------- |
| **Scope**       | Single interaction  | Ongoing behavior                 |
| **Purpose**     | Get specific output | Define agent personality & goals |
| **Flexibility** | Changes per request | Consistent across sessions       |

---

## 🚀 Models Used

### **gemini-2.5-flash-lite**

A fast, efficient version of Google's Gemini model optimized for agent applications.

**Characteristics**:

- Lower latency (faster responses)
- Cost-effective
- Good for prototyping and production
- Balances performance with efficiency

---

## 💡 Best Practices

### **When to Use Agents**

- Tasks requiring current/real-time information
- Multi-step processes needing planning
- Interactions with external systems/APIs
- Dynamic decision-making scenarios

### **When to Use Simple LLMs**

- Pure text generation tasks
- Static knowledge questions
- Creative writing
- One-shot completions

### **Instruction Writing Tips**

- Be clear about the agent's role
- Specify when to use tools
- Define expected behavior patterns
- Include fallback instructions

---

## 🐛 Debugging

### **run_debug() Method**

Simplified execution method that automatically:

- Creates or continues sessions
- Displays user input and agent responses
- Shows session IDs for tracking
- Handles basic error scenarios

**Output Format**:

```
### Created new session: debug_session_id
User > [Your question]
helpful_assistant > [Agent's response]
```

### **ADK Web UI**

Visual interface showing:

- Complete agent thought process
- Tool execution traces
- Conversation history
- Performance metrics

---

## 📚 Important Notes

### **Environment Variables**

- `GOOGLE_API_KEY`: Your Gemini API authentication
- `GOOGLE_GENAI_USE_VERTEXAI`: Set to "FALSE" for API usage (vs Vertex AI)

### **Security**

- Never share API keys publicly
- Don't share proxy URLs (contain auth tokens)
- Store credentials in secure secret management

### **Limitations**

- `run_debug()` is for prototyping, not production
- InMemoryRunner doesn't persist data across restarts
- Rate limits apply to API calls

---

## ✅ Day 1 Learning Outcomes

By completing Day 1, you now understand:

- ✅ The fundamental difference between LLMs and AI Agents
- ✅ How to configure and create an agent with ADK
- ✅ How tools extend agent capabilities
- ✅ The role of Runners in agent execution
- ✅ Basic agent workflow and reasoning process
- ✅ How to use ADK CLI and web interface

---

## 🔗 Additional Resources

- **ADK Documentation**: https://developers.google.com/adk
- **ADK Quickstart (Python)**: Official Python guide
- **ADK Agents Overview**: Deep dive into agent concepts
- **ADK Tools Overview**: Creating custom tools

---

## 🎯 Next: Day 2 Preview

Day 2 will cover **Multi-Agent Systems** - architecting systems where multiple specialized agents work together to solve complex problems.

**Key Topics**:

- Agent orchestration
- Task delegation
- Inter-agent communication
- Building agent hierarchies
