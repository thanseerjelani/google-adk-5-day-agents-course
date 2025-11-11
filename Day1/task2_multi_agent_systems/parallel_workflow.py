"""
Day 1 - Task 2: Parallel Multi-Agent Workflow
Course: Google ADK 5-Day AI Agents Intensive

This demonstrates concurrent execution where multiple agents run simultaneously.
Perfect for independent tasks that can happen at the same time to speed up workflow.
"""

from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search

# Research Agent 1: Technology Focus
tech_researcher = Agent(
    name="TechResearcher",
    model="gemini-2.5-flash-lite",
    instruction="""Research the latest AI/ML trends. Include 3 key developments,
the main companies involved, and the potential impact. Keep the report very concise (100 words).""",
    tools=[google_search],
    output_key="tech_research",  # Each researcher has unique output_key
)

print("✅ tech_researcher created.")

# Research Agent 2: Health Focus
health_researcher = Agent(
    name="HealthResearcher",
    model="gemini-2.5-flash-lite",
    instruction="""Research recent medical breakthroughs. Include 3 significant advances,
their practical applications, and estimated timelines. Keep the report concise (100 words).""",
    tools=[google_search],
    output_key="health_research",
)

print("✅ health_researcher created.")

# Research Agent 3: Finance Focus
finance_researcher = Agent(
    name="FinanceResearcher",
    model="gemini-2.5-flash-lite",
    instruction="""Research current fintech trends. Include 3 key trends,
their market implications, and the future outlook. Keep the report concise (100 words).""",
    tools=[google_search],
    output_key="finance_research",
)

print("✅ finance_researcher created.")

# Aggregator Agent: Combines all parallel results
aggregator_agent = Agent(
    name="AggregatorAgent",
    model="gemini-2.5-flash-lite",
    # Uses placeholders to inject ALL parallel agent outputs
    instruction="""Combine these three research findings into a single executive summary:

    **Technology Trends:**
    {tech_research}
    
    **Health Breakthroughs:**
    {health_research}
    
    **Finance Innovations:**
    {finance_research}
    
    Your summary should highlight common themes, surprising connections, 
    and the most important key takeaways from all three reports. 
    The final summary should be around 200 words.""",
    output_key="executive_summary",
)

print("✅ aggregator_agent created.")

# Parallel Agent: Runs all researchers simultaneously
parallel_research_team = ParallelAgent(
    name="ParallelResearchTeam",
    sub_agents=[
        tech_researcher,      # All three run
        health_researcher,    # at the exact
        finance_researcher    # same time
    ],
)

# Sequential Agent: First parallel research, then aggregation
root_agent = SequentialAgent(
    name="ResearchSystem",
    sub_agents=[
        parallel_research_team,  # Step 1: All 3 research in parallel
        aggregator_agent         # Step 2: Combine after all done
    ],
)

print("✅ Parallel and Sequential Agents created.")

# Execute the system
async def main():
    runner = InMemoryRunner(agent=root_agent)
    
    print("\n" + "="*70)
    print("EXAMPLE: Multi-Topic Executive Briefing")
    print("="*70)
    
    response = await runner.run_debug(
        "Run the daily executive briefing on Tech, Health, and Finance"
    )

# Key Learnings:
# 1. ParallelAgent - Runs all sub-agents concurrently (at same time)
# 2. Nesting patterns - Parallel inside Sequential for complex workflows
# 3. Each parallel agent needs unique output_key
# 4. Aggregator runs AFTER all parallel tasks complete

# Workflow Flow:
#                    ┌→ TechResearcher → tech_research ┐
# User Query → Parallel┼→ HealthResearcher → health_research ┼→ All Complete
#                    └→ FinanceResearcher → finance_research ┘
#                                          ↓
#                    AggregatorAgent (reads all 3) → executive_summary
#                                          ↓
#                                      Response

# State After Parallel (all 3 done):
# state = {
#     "tech_research": "...",
#     "health_research": "...",
#     "finance_research": "..."
# }

# Timing Comparison:
# Sequential: 3 agents × 5 seconds each = 15 seconds total
# Parallel:   3 agents running together = ~5 seconds total (3x faster!)

# Pros: Fast, efficient, great for independent tasks
# Cons: Uses more API quota (3 simultaneous calls), needs more resources

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())