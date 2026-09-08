from server.services.mcp.mcp_tool_service import execute_mcp_tool

# Tools exposed over MCP. The MCP tool name matches the local tool
# function name, so this is an allowlist rather than a translation table.
ALLOWED_MCP_TOOLS = {
    "gmail_list_messages",
    "calendar_get_upcoming_events",
    "github_list_repositories",
}


def execute_mcp_tools(tool_calls):
    results = []

    for tool_call in tool_calls:
        tool_name = tool_call.tool.__name__

        if tool_name not in ALLOWED_MCP_TOOLS:
            results.append({
                "success": False,
                "error": f"No MCP mapping found for {tool_name}",
            })
            continue

        mcp_tool_name = tool_name

        try:
            result = execute_mcp_tool(mcp_tool_name)

            if isinstance(result, list):
                result = "\n".join(
                    item.text if hasattr(item, "text") else str(item)
                    for item in result
                )
            elif hasattr(result, "text"):
                result = result.text

            results.append({
                "success": True,
                "tool": mcp_tool_name,
                "result": result,
            })

        except Exception as exc:
            results.append({
                "success": False,
                "tool": mcp_tool_name,
                "error": str(exc),
            })

    return results
