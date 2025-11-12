"""
Day 2 - Exercise: Image Generation Agent with Interactive Human Approval

Features:
- Single image (1): Auto-approve and generate immediately
- Bulk images (>1): Pause and ask for INTERACTIVE human approval
- Display generated images in notebook
- Real yes/no input from user

This combines:
- MCP integration (image generation server)
- Long-Running Operations (approval workflow)
- Interactive human input
- Image display functionality
"""

# ============================================================================
# SECTION 1: SETUP & IMPORTS
# ============================================================================

import os
import uuid
import base64
from IPython.display import display, Image as IPImage
from kaggle_secrets import UserSecretsClient
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from google.adk.tools import ToolContext, FunctionTool
from google.adk.apps.app import App, ResumabilityConfig

# Authenticate
try:
    GOOGLE_API_KEY = UserSecretsClient().get_secret("GOOGLE_API_KEY")
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
    print("✅ Setup and authentication complete.")
except Exception as e:
    print(f"🔑 Authentication Error: {e}")

# Configure retry options
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

print("✅ ADK components imported successfully.")


# ============================================================================
# SECTION 2: MCP IMAGE GENERATION TOOLSET
# ============================================================================

# Using the Everything MCP Server for demo
mcp_image_generator = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-everything"],
            tool_filter=["getTinyImage"],  # Image generation tool
        ),
        timeout=30,
    )
)

print("✅ MCP Image Generator Toolset created")


# ============================================================================
# SECTION 3: CUSTOM LONG-RUNNING OPERATION TOOL
# ============================================================================

# Threshold for bulk image generation
BULK_IMAGE_THRESHOLD = 1  # More than 1 image = bulk = needs approval

def generate_images_with_approval(
    num_images: int,
    description: str,
    tool_context: ToolContext
) -> dict:
    """
    Generates images with approval workflow for bulk requests.
    
    Workflow:
    - 1 image: Auto-approve immediately
    - >1 images: Pause and request human approval
    
    Args:
        num_images: Number of images to generate
        description: Description of images to generate
        tool_context: ADK-provided context (automatic)
    
    Returns:
        Status dictionary with generation details
    """
    
    # SCENARIO 1: Single image - auto-approve
    if num_images <= BULK_IMAGE_THRESHOLD:
        return {
            "status": "approved",
            "generation_id": f"IMG-{num_images}-AUTO",
            "num_images": num_images,
            "description": description,
            "message": f"Auto-approved: Ready to generate {num_images} image",
            "cost_estimate": f"${num_images * 0.02:.2f}",
        }
    
    # SCENARIO 2: First call - bulk request - PAUSE for approval
    if not tool_context.tool_confirmation:
        cost_estimate = num_images * 0.02  # $0.02 per image
        tool_context.request_confirmation(
            hint=f"💰 Bulk Generation Request:\n"
                 f"  • Images: {num_images}\n"
                 f"  • Description: {description}\n"
                 f"  • Estimated Cost: ${cost_estimate:.2f}\n"
                 f"  • Approve this bulk generation?",
            payload={
                "num_images": num_images,
                "description": description,
                "cost_estimate": cost_estimate
            }
        )
        return {
            "status": "pending",
            "message": f"Bulk generation of {num_images} images requires approval",
            "cost_estimate": f"${cost_estimate:.2f}"
        }
    
    # SCENARIO 3: Resumed call - handle approval decision
    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "approved",
            "generation_id": f"IMG-{num_images}-HUMAN",
            "num_images": num_images,
            "description": description,
            "message": f"✅ Approved: Ready to generate {num_images} images",
            "cost_estimate": f"${num_images * 0.02:.2f}",
        }
    else:
        return {
            "status": "rejected",
            "num_images": num_images,
            "message": f"❌ Rejected: Bulk generation of {num_images} images cancelled",
        }


print("✅ Custom approval tool created")


# ============================================================================
# SECTION 4: CREATE IMAGE GENERATION AGENT
# ============================================================================

image_generation_agent = LlmAgent(
    name="image_generation_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are an AI image generation assistant with cost awareness.

    For image generation requests:
    
    1. First, use the `generate_images_with_approval` tool to check if approval is needed
       - Extract the number of images from user request
       - Pass the number and description
    
    2. Check the response status:
       - If "approved": Inform user and proceed to generate
       - If "pending": Inform user that approval is required and WAIT
       - If "rejected": Inform user the request was cancelled, do NOT generate
    
    3. For approved requests ONLY:
       - Use the getTinyImage tool from MCP to generate the image(s)
       - Call getTinyImage once for each approved image
       - Inform user about generation progress
    
    4. Always provide:
       - Clear status updates
       - Number of images
       - Estimated cost
       - Generation ID (if applicable)
    
    IMPORTANT: Only call getTinyImage AFTER approval is confirmed!
    """,
    tools=[
        FunctionTool(func=generate_images_with_approval),
        mcp_image_generator,
    ],
)

print("✅ Image Generation Agent created")


# ============================================================================
# SECTION 5: CREATE RESUMABLE APP
# ============================================================================

image_generation_app = App(
    name="image_generation_coordinator",
    root_agent=image_generation_agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)

print("✅ Resumable App created")


# ============================================================================
# SECTION 6: CREATE SESSION SERVICE AND RUNNER
# ============================================================================

session_service = InMemorySessionService()

image_runner = Runner(
    app=image_generation_app,
    session_service=session_service,
)

print("✅ Runner created with resumable app")


# ============================================================================
# SECTION 7: HELPER FUNCTIONS FOR WORKFLOW
# ============================================================================

def check_for_approval(events) -> dict | None:
    """Check if events contain an approval request."""
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if (
                    part.function_call
                    and part.function_call.name == "adk_request_confirmation"
                ):
                    return {
                        "approval_id": part.function_call.id,
                        "invocation_id": event.invocation_id,
                        "hint": part.function_call.args.get("hint", "")
                    }
    return None


def create_approval_response(approval_info: dict, approved: bool) -> types.Content:
    """Create approval response message."""
    confirmation_response = types.FunctionResponse(
        id=approval_info["approval_id"],
        name="adk_request_confirmation",
        response={"confirmed": approved},
    )
    return types.Content(
        role="user",
        parts=[types.Part(function_response=confirmation_response)]
    )


def print_agent_response(events):
    """Print agent's text responses from events."""
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"🤖 Agent > {part.text}")


def extract_and_display_images(events):
    """Extract and display images from events."""
    images_found = False
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "function_response") and part.function_response:
                    response_content = part.function_response.response
                    if isinstance(response_content, dict):
                        content_items = response_content.get("content", [])
                        for item in content_items:
                            if isinstance(item, dict) and item.get("type") == "image":
                                images_found = True
                                print("\n🖼️ Generated Image:")
                                try:
                                    image_data = base64.b64decode(item["data"])
                                    display(IPImage(data=image_data))
                                except Exception as e:
                                    print(f"   ⚠️ Error displaying image: {e}")
    
    if not images_found:
        print("\n   ℹ️ No images found in response")
    
    return images_found


def get_human_approval() -> bool:
    """
    Get interactive human approval via input.
    
    Returns:
        True if approved, False if rejected
    """
    print("\n" + "="*70)
    print("⏸️  APPROVAL REQUIRED")
    print("="*70)
    
    while True:
        response = input("\n👤 Do you approve this request? (yes/no): ").strip().lower()
        
        if response in ['yes', 'y']:
            print("✅ You approved the request")
            return True
        elif response in ['no', 'n']:
            print("❌ You rejected the request")
            return False
        else:
            print("⚠️  Please enter 'yes' or 'no'")


print("✅ Helper functions defined")


# ============================================================================
# SECTION 8: MAIN WORKFLOW FUNCTION WITH INTERACTIVE APPROVAL
# ============================================================================

async def run_image_generation_workflow(query: str, interactive: bool = False, auto_approve: bool = True):
    """
    Runs the image generation workflow with approval handling.
    
    Args:
        query: User's image generation request
        interactive: If True, ask for human input. If False, use auto_approve
        auto_approve: Whether to auto-approve (only used if interactive=False)
    """
    
    print(f"\n{'='*70}")
    print(f"👤 User > {query}\n")
    
    # Generate unique session ID
    session_id = f"img_gen_{uuid.uuid4().hex[:8]}"
    
    # Create session
    await session_service.create_session(
        app_name="image_generation_coordinator",
        user_id="test_user",
        session_id=session_id
    )
    
    query_content = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )
    
    all_events = []
    
    # STEP 1: Send initial request to agent
    print("🔄 Processing request...")
    async for event in image_runner.run_async(
        user_id="test_user",
        session_id=session_id,
        new_message=query_content
    ):
        all_events.append(event)
    
    # Print agent's initial response
    print_agent_response(all_events)
    
    # STEP 2: Check if approval is needed
    approval_info = check_for_approval(all_events)
    
    # STEP 3: Handle approval workflow if needed
    if approval_info:
        print(f"\n⏸️  PAUSED for approval")
        print(f"\n💭 Request Details:")
        print(approval_info["hint"])
        
        # Get approval decision
        if interactive:
            # Interactive mode - ask human
            approved = get_human_approval()
        else:
            # Auto mode - use parameter
            print(f"\n🤖 Auto Decision: {'✅ APPROVE' if auto_approve else '❌ REJECT'}")
            approved = auto_approve
        
        print(f"\n🔄 Resuming workflow with {'approval' if approved else 'rejection'}...\n")
        
        # Resume with human decision
        resumed_events = []
        async for event in image_runner.run_async(
            user_id="test_user",
            session_id=session_id,
            new_message=create_approval_response(approval_info, approved),
            invocation_id=approval_info["invocation_id"],
        ):
            resumed_events.append(event)
        
        # Print agent's response after resume
        print_agent_response(resumed_events)
        
        # Combine all events for image extraction
        all_events.extend(resumed_events)
    
    # STEP 4: Display any generated images
    if approval_info is None or (approval_info and approved):
        print("\n" + "="*70)
        print("🎨 IMAGE GENERATION")
        print("="*70)
        extract_and_display_images(all_events)
    
    print(f"{'='*70}\n")


print("✅ Workflow function ready")


# ============================================================================
# SECTION 9: TEST SCENARIOS
# ============================================================================

print("\n" + "="*70)
print("🎨 IMAGE GENERATION AGENT WITH COST APPROVAL")
print("="*70)
print("\nRunning automated test scenarios...\n")


# TEST 1: Single image - should auto-approve and generate
print("📝 TEST 1: Single Image Request (Auto-approve)")
print("-" * 70)
await run_image_generation_workflow(
    "Generate 1 image of a sunset over mountains",
    interactive=False,
    auto_approve=True
)


# TEST 2: Bulk images with auto-approval
print("\n📝 TEST 2: Bulk Image Request - Auto Approved")
print("-" * 70)
await run_image_generation_workflow(
    "Generate 3 images of abstract art patterns",
    interactive=False,
    auto_approve=True
)


# TEST 3: Bulk images auto-rejected
print("\n📝 TEST 3: Bulk Image Request - Auto Rejected")
print("-" * 70)
await run_image_generation_workflow(
    "Generate 5 images of city landscapes",
    interactive=False,
    auto_approve=False
)


# ============================================================================
# SECTION 10: INTERACTIVE MODE (Run this separately!)
# ============================================================================

print("\n" + "="*70)
print("🎮 INTERACTIVE MODE")
print("="*70)
print("\nNow YOU control the approvals!")
print("Run the cell below to test with real human input:\n")

# Uncomment and run this cell separately to test interactive mode:
"""
# INTERACTIVE TEST: You decide!
await run_image_generation_workflow(
    "Generate 4 images of futuristic cities",
    interactive=True  # This will ask for your yes/no input!
)
"""

print("\n✅ All automated tests complete!")
print("\n📊 SUMMARY")
print("="*70)
print("""
What This Exercise Demonstrates:

✅ MCP Integration
   - Connected to Everything MCP Server
   - Used getTinyImage tool for actual image generation
   - Images displayed in notebook output

✅ Long-Running Operations
   - Implemented approval workflow for bulk requests
   - Used ToolContext for pause/resume
   - State managed across pause/resume cycles

✅ Interactive Human Approval
   - Real yes/no input from user
   - Approval workflow pauses until human responds
   - Decision integrated into agent execution

✅ Cost Awareness
   - Calculated cost estimates ($0.02 per image)
   - Required approval for expensive operations
   - Clear cost display before approval

✅ Three Scenarios Tested
   - Single image: Auto-approved immediately ✅
   - Bulk approved: Paused → Approved → Generated ✅
   - Bulk rejected: Paused → Rejected → Cancelled ✅

✅ Production Patterns
   - Resumable App configuration
   - Event detection and handling
   - Image extraction and display
   - Structured workflow with invocation_id

🎮 Interactive Mode Available
   - Uncomment Section 10 code to test with real input
   - You'll be asked "Do you approve? (yes/no)"
   - Agent responds based on YOUR decision

Key Learnings:
- Combining MCP tools with custom LRO tools
- Building cost-conscious AI agents
- Implementing interactive approval gates
- Managing state across pause/resume cycles
- Extracting and displaying generated content

🎉 Exercise Complete! Ready for Day 3!
""")