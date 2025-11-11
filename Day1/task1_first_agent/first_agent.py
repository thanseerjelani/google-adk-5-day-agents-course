"""
Day 1 - Task 1: First AI Agent with Google Search Tool
Course: Google ADK 5-Day AI Agents Intensive

This script demonstrates building a basic AI agent that can:
- Use the Google Search tool to find current information
- Answer questions requiring real-time data
"""

import os
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types

# Note: Set your API key as environment variable
# export GOOGLE_API_KEY="your-api-key-here"

# Define the agent with Google Search capability
root_agent = Agent(
    name="helpful_assistant",
    model="gemini-2.5-flash-lite",
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],  # This gives the agent ability to search the web
)

print("✅ Root Agent defined.")

# Create a runner to execute the agent
runner = InMemoryRunner(agent=root_agent)
print("✅ Runner created.")

async def run_agent_query(query):
    """
    Run a query through the agent and get response
    
    Args:
        query (str): The question to ask the agent
    
    Returns:
        Response from the agent
    """
    response = await runner.run_debug(query)
    return response

# Example queries demonstrating agent capabilities
async def main():
    """Main function to demonstrate various agent queries"""
    
    print("\n" + "="*60)
    print("EXAMPLE 1: Asking about Agent Development Kit")
    print("="*60)
    await run_agent_query(
        "What is Agent Development Kit from Google? What languages is the SDK available in?"
    )
    
    print("\n" + "="*60)
    print("EXAMPLE 2: Current information query")
    print("="*60)
    await run_agent_query("What's the weather in London?")
    
    print("\n" + "="*60)
    print("EXAMPLE 3: Recent events")
    print("="*60)
    await run_agent_query("Who won the last soccer world cup?")

# Key Learnings:
# 1. Agent = The AI entity with specific capabilities
# 2. tools=[google_search] = Gives agent ability to search web
# 3. InMemoryRunner = Executes the agent and manages conversation
# 4. run_debug() = Quick method for prototyping without session management

# To run this script:
# python first_agent.py
# (Make sure to run in an async context or Jupyter notebook)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())