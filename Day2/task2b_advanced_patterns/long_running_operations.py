"""
Day 2 - Task 2B: Long-Running Operations (Human-in-the-Loop)

Demonstrates:
- Tools that pause for human approval
- Resumable workflows
- ToolContext for pause/resume
- App with resumability configuration
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import ToolContext, FunctionTool
from google.adk.apps.app import App, ResumabilityConfig
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

LARGE_ORDER_THRESHOLD = 5

def place_shipping_order(num_containers: int, destination: str, tool_context: ToolContext) -> dict:
    """Places shipping order with approval for large orders.
    
    Three scenarios:
    1. Small order (≤5): Auto-approve immediately
    2. Large order - First call: Pause and request approval
    3. Large order - Resume: Complete based on human decision
    """
    
    # SCENARIO 1: Small order - auto-approve
    if num_containers <= LARGE_ORDER_THRESHOLD:
        return {
            "status": "approved",
            "order_id": f"ORD-{num_containers}-AUTO",
            "message": f"Auto-approved: {num_containers} containers to {destination}"
        }
    
    # SCENARIO 2: First call - PAUSE for approval
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"⚠️ Large order: {num_containers} containers to {destination}. Approve?",
            payload={"num_containers": num_containers, "destination": destination}
        )
        return {"status": "pending", "message": "Requires approval"}
    
    # SCENARIO 3: Resume - handle decision
    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "approved",
            "order_id": f"ORD-{num_containers}-HUMAN",
            "message": f"Order approved: {num_containers} containers to {destination}"
        }
    return {"status": "rejected", "message": "Order rejected"}


# Create agent
shipping_agent = LlmAgent(
    name="shipping_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction="""Shipping coordinator assistant.
    
    Use place_shipping_order tool for requests.
    If status is 'pending', inform user approval is required.
    Provide clear summary after completion.
    """,
    tools=[FunctionTool(func=place_shipping_order)]
)

# CRITICAL: Wrap in resumable App
shipping_app = App(
    name="shipping_coordinator",
    root_agent=shipping_agent,
    resumability_config=ResumabilityConfig(is_resumable=True)  # Enables pause/resume
)

# Create runner with App (not Agent!)
shipping_runner = Runner(
    app=shipping_app,  # Pass app for resumability
    session_service=InMemorySessionService()
)

# Key Learnings:
# - ToolContext enables pause/resume
# - request_confirmation() pauses execution
# - tool_confirmation contains human decision
# - App + ResumabilityConfig saves state
# - invocation_id ties pause and resume together