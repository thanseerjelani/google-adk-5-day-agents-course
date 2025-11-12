"""
Day 2 - Task 2A: Code Execution for Reliable Calculations

Demonstrates:
- BuiltInCodeExecutor usage
- Agent as tool pattern (AgentTool)
- Delegation to specialist agents
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.tools import AgentTool

# Specialist agent for calculations
calculation_agent = LlmAgent(
    name="CalculationAgent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction="""You ONLY respond with Python code.
    
    RULES:
    1. Output MUST be ONLY a Python code block
    2. NO text before or after code
    3. Code MUST calculate the result
    4. Code MUST print final result to stdout
    5. PROHIBITED from doing calculation yourself
    """,
    code_executor=BuiltInCodeExecutor()  # Enables code execution
)

# Main agent that uses calculator as a tool
enhanced_agent = LlmAgent(
    name="enhanced_currency_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction="""Currency conversion assistant.
    
    CRITICAL: You are PROHIBITED from doing arithmetic yourself.
    Use calculation_agent to generate and run Python code.
    """,
    tools=[
        get_fee_for_payment_method,
        get_exchange_rate,
        AgentTool(agent=calculation_agent)  # Use specialist as tool!
    ]
)

# Key Learnings:
# - Code execution more reliable than LLM math
# - AgentTool() wraps agents as callable tools
# - Specialist agents handle specific tasks
# - Result flows back to calling agent