"""
Day 1 - Task 2: Sequential Multi-Agent Workflow
Course: Google ADK 5-Day AI Agents Intensive

This demonstrates a fixed-order pipeline where agents run one after another.
Perfect for workflows where order matters and each step builds on the previous.
"""

from google.adk.agents import Agent, SequentialAgent
from google.adk.runners import InMemoryRunner

# Agent 1: Outline Creator
outline_agent = Agent(
    name="OutlineAgent",
    model="gemini-2.5-flash-lite",
    instruction="""Create a blog outline for the given topic with:
    1. A catchy headline
    2. An introduction hook
    3. 3-5 main sections with 2-3 bullet points for each
    4. A concluding thought""",
    output_key="blog_outline",  # Saves outline here
)

print("✅ outline_agent created.")

# Agent 2: Blog Writer
writer_agent = Agent(
    name="WriterAgent",
    model="gemini-2.5-flash-lite",
    # Reads {blog_outline} from outline_agent's output
    instruction="""Following this outline strictly: {blog_outline}
    Write a brief, 200 to 300-word blog post with an engaging and informative tone.""",
    output_key="blog_draft",  # Saves draft here
)

print("✅ writer_agent created.")

# Agent 3: Editor
editor_agent = Agent(
    name="EditorAgent",
    model="gemini-2.5-flash-lite",
    # Reads {blog_draft} from writer_agent's output
    instruction="""Edit this draft: {blog_draft}
    Your task is to polish the text by fixing any grammatical errors, 
    improving the flow and sentence structure, and enhancing overall clarity.""",
    output_key="final_blog",  # Saves final version here
)

print("✅ editor_agent created.")

# Sequential Agent: Runs agents in fixed order
root_agent = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[
        outline_agent,   # Step 1: Create outline
        writer_agent,    # Step 2: Write based on outline
        editor_agent     # Step 3: Edit the draft
    ],
)

print("✅ Sequential Agent created.")

# Execute the pipeline
async def main():
    runner = InMemoryRunner(agent=root_agent)
    
    print("\n" + "="*70)
    print("EXAMPLE: Creating a Blog Post")
    print("="*70)
    
    response = await runner.run_debug(
        "Write a blog post about the benefits of multi-agent systems for software developers"
    )

# Key Learnings:
# 1. SequentialAgent - Guarantees execution order (assembly line pattern)
# 2. Data flows automatically through output_key → {placeholder}
# 3. Each agent builds on previous agent's work
# 4. Deterministic and predictable

# Workflow Flow:
# User Topic → OutlineAgent (creates outline) → blog_outline
#           → WriterAgent (reads blog_outline, writes draft) → blog_draft
#           → EditorAgent (reads blog_draft, edits) → final_blog
#           → Response to user

# State Evolution:
# After outline_agent: state = {"blog_outline": "..."}
# After writer_agent:  state = {"blog_outline": "...", "blog_draft": "..."}
# After editor_agent:  state = {"blog_outline": "...", "blog_draft": "...", "final_blog": "..."}

# Pros: Predictable, reliable, easy to debug
# Cons: Slow (must wait for each step), can't parallelize

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())