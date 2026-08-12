from server.services.mcp.mcp_tool_service import execute_mcp_tool


TOOL_MAPPING = {
    "gmail_list_messages": "gmail_list_messages",
    "calendar_get_upcoming_events": "calendar_get_upcoming_events",
    "github_list_repositories": "github_list_repositories",
}


def execute_mcp_tools(tool_calls):
    results = []

    for tool_call in tool_calls:
        tool_name = tool_call.tool.__name__

        mcp_tool_name = TOOL_MAPPING.get(tool_name)

        if not mcp_tool_name:
            results.append({
                "success": False,
                "error": f"No MCP mapping found for {tool_name}",
            })
            continue

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