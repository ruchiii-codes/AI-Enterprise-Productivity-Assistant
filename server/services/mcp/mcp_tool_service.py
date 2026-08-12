import asyncio

from server.services.mcp.mcp_client import call_mcp_tool


def execute_mcp_tool(tool_name: str):
    return asyncio.run(call_mcp_tool(tool_name))