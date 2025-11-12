"""
Helper functions for long-running operation workflows.

These detect pauses, format responses, and handle approvals.
"""

from google.genai import types

def check_for_approval(events) -> dict | None:
    """Check if events contain approval request.
    
    Returns:
        {"approval_id": "...", "invocation_id": "..."} or None
    """
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.function_call and part.function_call.name == "adk_request_confirmation":
                    return {
                        "approval_id": part.function_call.id,
                        "invocation_id": event.invocation_id
                    }
    return None


def create_approval_response(approval_info: dict, approved: bool) -> types.Content:
    """Create approval response message for resuming.
    
    Args:
        approval_info: Dict with approval_id and invocation_id
        approved: Boolean decision from human
    
    Returns:
        Content object to send to agent
    """
    confirmation_response = types.FunctionResponse(
        id=approval_info["approval_id"],
        name="adk_request_confirmation",
        response={"confirmed": approved}
    )
    return types.Content(
        role="user",
        parts=[types.Part(function_response=confirmation_response)]
    )


def print_agent_response(events):
    """Extract and print agent's text responses from events."""
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"Agent > {part.text}")