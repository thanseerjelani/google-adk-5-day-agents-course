"""
Reusable template for long-running operation tools.

Use this when you need human approval or external input.
"""

from google.adk.tools import ToolContext

APPROVAL_THRESHOLD = 10  # [REPLACE] Your threshold

def my_lro_tool(item_count: int, tool_context: ToolContext) -> dict:
    """[REPLACE] Tool that requires approval for large operations.
    
    Args:
        item_count: [REPLACE] Number of items to process
        tool_context: ADK-provided context (automatic)
    
    Returns:
        Status dictionary
    """
    
    # SCENARIO 1: Below threshold - auto-approve
    if item_count <= APPROVAL_THRESHOLD:
        return {
            "status": "approved",
            "id": f"AUTO-{item_count}",
            "message": f"Auto-approved: {item_count} items"
        }
    
    # SCENARIO 2: First call - request approval
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"⚠️ Large operation: {item_count} items. Approve?",
            payload={"item_count": item_count}  # [REPLACE] Your data
        )
        return {
            "status": "pending",
            "message": f"{item_count} items requires approval"
        }
    
    # SCENARIO 3: Resumed - handle decision
    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "approved",
            "id": f"HUMAN-{item_count}",
            "message": f"Approved: {item_count} items"
        }
    else:
        return {
            "status": "rejected",
            "message": f"Rejected: {item_count} items"
        }

# Setup Requirements:
# 1. Wrap agent in App with ResumabilityConfig(is_resumable=True)
# 2. Use Runner(app=app) not Runner(agent=agent)
# 3. Workflow must detect adk_request_confirmation event
# 4. Resume with same invocation_id