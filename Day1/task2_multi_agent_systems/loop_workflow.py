"""
Day 1 - Task 2: Loop Multi-Agent Workflow
Course: Google ADK 5-Day AI Agents Intensive

This demonstrates iterative refinement where agents repeatedly review and improve
work until it meets quality standards. Perfect for tasks requiring polish and iteration.
"""

from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool

# Agent 1: Initial Writer (runs once at start)
initial_writer_agent = Agent(
    name="InitialWriterAgent",
    model="gemini-2.5-flash-lite",
    instruction="""Based on the user's prompt, write the first draft of a short story (around 100-150 words).
    Output only the story text, with no introduction or explanation.""",
    output_key="current_story",  # Creates first version
)

print("✅ initial_writer_agent created.")

# Agent 2: Critic (reviews the story)
critic_agent = Agent(
    name="CriticAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are a constructive story critic. Review the story provided below.
    Story: {current_story}
    
    Evaluate the story's plot, characters, and pacing.
    - If the story is well-written and complete, you MUST respond with the exact phrase: "APPROVED"
    - Otherwise, provide 2-3 specific, actionable suggestions for improvement.""",
    output_key="critique",  # Stores feedback
)

print("✅ critic_agent created.")

# Exit Function: Signals loop to stop
def exit_loop():
    """
    Call this function ONLY when the critique is 'APPROVED', 
    indicating the story is finished and no more changes are needed.
    """
    return {"status": "approved", "message": "Story approved. Exiting refinement loop."}

print("✅ exit_loop function created.")

# Agent 3: Refiner (improves story or exits)
refiner_agent = Agent(
    name="RefinerAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are a story refiner. You have a story draft and critique.
    
    Story Draft: {current_story}
    Critique: {critique}
    
    Your task is to analyze the critique.
    - IF the critique is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
    - OTHERWISE, rewrite the story draft to fully incorporate the feedback from the critique.""",
    
    output_key="current_story",  # OVERWRITES story with improved version
    tools=[FunctionTool(exit_loop)],  # Can call exit function
)

print("✅ refiner_agent created.")

# Loop Agent: Repeats critic → refiner cycle
story_refinement_loop = LoopAgent(
    name="StoryRefinementLoop",
    sub_agents=[
        critic_agent,    # Reviews current story
        refiner_agent    # Improves or exits
    ],
    max_iterations=2,  # Safety limit (prevents infinite loops)
)

# Sequential Agent: Initial write, then refinement loop
root_agent = SequentialAgent(
    name="StoryPipeline",
    sub_agents=[
        initial_writer_agent,  # Runs once to create first draft
        story_refinement_loop  # Loops until approved or max_iterations
    ],
)

print("✅ Loop and Sequential Agents created.")

# Execute the system
async def main():
    runner = InMemoryRunner(agent=root_agent)
    
    print("\n" + "="*70)
    print("EXAMPLE: Iterative Story Refinement")
    print("="*70)
    
    response = await runner.run_debug(
        "Write a short story about a lighthouse keeper who discovers a mysterious, glowing map"
    )

# Key Learnings:
# 1. LoopAgent - Repeats sub-agents until condition met or max_iterations
# 2. FunctionTool - Wraps Python functions so agents can call them
# 3. output_key overwriting - refiner_agent OVERWRITES current_story each iteration
# 4. Exit conditions - Need explicit signal (exit_loop function) to stop

# Workflow Flow:
# User Prompt → InitialWriterAgent → current_story (v1)
#                                      ↓
#                        ┌─────── LOOP STARTS ───────┐
#                        │                           │
#                   CriticAgent (reviews)            │
#                        ↓                           │
#                   critique                         │
#                        ↓                           │
#                   RefinerAgent                     │
#                   ├─ If "APPROVED" → exit_loop()   │ (stops loop)
#                   └─ Else → rewrite → current_story (v2)
#                        ↑___________________________|
#                                 (repeats)
#
# Final: current_story (final version) → Response

# Iteration Example:
# Iteration 1:
#   - current_story: "Draft 1 text..."
#   - critique: "Needs better character development, more tension..."
#   - current_story: "Draft 2 text..." (improved version)
#
# Iteration 2:
#   - current_story: "Draft 2 text..."
#   - critique: "APPROVED"
#   - exit_loop() called → Loop stops

# State Changes:
# Initial:        state = {"current_story": "Draft 1..."}
# After Loop 1:   state = {"current_story": "Draft 2...", "critique": "Improve X..."}
# After Loop 2:   state = {"current_story": "Draft 2...", "critique": "APPROVED"}
# (Loop exits)

# Pros: Quality improvement through iteration, self-correcting
# Cons: Uses more API calls, slower, needs max_iterations safety

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())