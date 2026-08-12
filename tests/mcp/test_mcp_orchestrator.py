from unittest.mock import patch

from server.services.mcp.mcp_orchestrator import execute_mcp_tools
from server.services.multi_tool.tool_call import ToolCall
from server.services.integrations.github.github_tool import github_list_repositories


def test_execute_mcp_tools():
    tool_calls = [
        ToolCall(tool=github_list_repositories),
    ]

    with patch(
        "server.services.mcp.mcp_orchestrator.execute_mcp_tool",
        return_value=["GitHub result"],
    ):
        results = execute_mcp_tools(tool_calls)

    assert results == [
        {
            "success": True,
            "tool": "github_list_repositories",
            "result": "GitHub result",
        }
    ]