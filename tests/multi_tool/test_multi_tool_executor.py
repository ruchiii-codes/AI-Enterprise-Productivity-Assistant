from server.services.multi_tool.multi_tool_executor import execute_multiple_tools
from server.services.multi_tool.tool_call import ToolCall


def test_execute_multiple_tools():
    def gmail_tool():
        return "Gmail result"

    def calendar_tool():
        return "Calendar result"

    tool_calls = [
        ToolCall(tool=gmail_tool),
        ToolCall(tool=calendar_tool),
    ]

    results = execute_multiple_tools(tool_calls)

    assert results == [
        {
            "success": True,
            "tool": "gmail_tool",
            "result": "Gmail result",
        },
        {
            "success": True,
            "tool": "calendar_tool",
            "result": "Calendar result",
        },
    ]


def test_execute_multiple_tools_handles_failure():
    def working_tool():
        return "Working"

    def failing_tool():
        raise RuntimeError("Tool failed")

    tool_calls = [
        ToolCall(tool=working_tool),
        ToolCall(tool=failing_tool),
    ]

    results = execute_multiple_tools(tool_calls)

    assert results[0] == {
        "success": True,
        "tool": "working_tool",
        "result": "Working",
    }

    assert results[1] == {
        "success": False,
        "tool": "failing_tool",
        "result": None,
        "error": "Tool failed",
    }