"""
Day 1 - Task 2: LLM-Based Multi-Agent Orchestration
Course: Google ADK 5-Day AI Agents Intensive

This demonstrates using an LLM as a "manager" to dynamically coordinate
specialized sub-agents. The root agent decides which agents to call and when.
"""

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, google_search

# Sub-Agent 1: Research Agent
# Specialized in finding information using Google Search
research_agent = Agent(
    name="ResearchAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are a specialized research agent. Your only job is to use the
    google_search tool to find 2-3 pieces of relevant information on the given topic 
    and present the findings with citations.""",
    tools=[google_search],
    output_key="research_findings",  # Stores results in session state
)

print("✅ research_agent created.")

# Sub-Agent 2: Summarizer Agent
# Specialized in creating concise summaries
summarizer_agent = Agent(
    name="SummarizerAgent",
    model="gemini-2.5-flash-lite",
    # Uses {research_findings} placeholder to access research_agent's output
    instruction="""Read the provided research findings: {research_findings}
Create a concise summary as a bulleted list with 3-5 key points.""",
    output_key="final_summary",
)

print("✅ summarizer_agent created.")

# Root Coordinator Agent
# Orchestrates the workflow by calling sub-agents as tools
root_agent = Agent(
    name="ResearchCoordinator",
    model="gemini-2.5-flash-lite",
    instruction="""You are a research coordinator. Your goal is to answer the user's query by orchestrating a workflow.
1. First, you MUST call the `ResearchAgent` tool to find relevant information on the topic provided by the user.
2. Next, after receiving the research findings, you MUST call the `SummarizerAgent` tool to create a concise summary.
3. Finally, present the final summary clearly to the user as your response.""",
    # Wrap sub-agents in AgentTool to make them callable
    tools=[
        AgentTool(research_agent),     # Makes research_agent callable
        AgentTool(summarizer_agent)    # Makes summarizer_agent callable
    ],
)

print("✅ root_agent created.")

# Create runner and execute
async def main():
    runner = InMemoryRunner(agent=root_agent)
    
    print("\n" + "="*70)
    print("EXAMPLE: Researching Quantum Computing and AI")
    print("="*70)
    
    response = await runner.run_debug(
        "What are the latest advancements in quantum computing and what do they mean for AI?"
    )

# Key Learnings:
# 1. AgentTool(agent) - Wraps an agent so other agents can call it
# 2. output_key - Names where agent stores its results in session state
# 3. {placeholder} - Injects data from session state into instructions
# 4. LLM decides workflow - Root agent's LLM determines which tools to call

# Workflow Flow:
# User Query → Root Agent → Decides to call ResearchAgent → Gets research_findings
#           → Root Agent → Decides to call SummarizerAgent → Gets final_summary
#           → Root Agent → Presents final_summary to user

# Pros: Flexible, can adapt to different queries
# Cons: Less predictable, might skip steps if LLM makes mistakes

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())