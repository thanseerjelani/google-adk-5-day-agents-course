"""
Day 2 - Task 2B: Model Context Protocol Integration

Demonstrates:
- Connecting to MCP servers
- Using community-built tools
- Standard protocol for external services
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Create MCP Toolset for Everything Server
mcp_image_server = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-everything"],
            tool_filter=["getTinyImage"]  # Only use specific tools
        ),
        timeout=30
    )
)

# Agent with MCP tools
image_agent = LlmAgent(
    name="image_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction="Use MCP tool to generate images",
    tools=[mcp_image_server]
)

# Key Learnings:
# - MCP = standardized way to connect to external services
# - No custom API client code needed
# - Community-built servers available
# - Same pattern works for GitHub, Slack, databases, etc.

# Examples of other MCP servers:
"""
# Kaggle MCP
McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command='npx',
            args=['-y', 'mcp-remote', 'https://www.kaggle.com/mcp']
        )
    )
)

# GitHub MCP (HTTP-based)
McpToolset(
    connection_params=StreamableHTTPServerParams(
        url="https://api.githubcopilot.com/mcp/",
        headers={"Authorization": f"Bearer {token}"}
    )
)
"""