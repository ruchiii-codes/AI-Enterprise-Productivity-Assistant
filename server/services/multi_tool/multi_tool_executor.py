from server.services.multi_tool.tool_call import ToolCall


def execute_multiple_tools(tool_calls: list[ToolCall]):
    """
    Execute multiple tool calls independently.
    """

    results = []

    for tool_call in tool_calls:
        try:
            result = tool_call.tool(**tool_call.args)

            results.append({
                "success": True,
                "tool": tool_call.tool.__name__,
                "result": result,
            })

        except Exception as exc:
            results.append({
                "success": False,
                "tool": tool_call.tool.__name__,
                "result": None,
                "error": str(exc),
            })

    return results