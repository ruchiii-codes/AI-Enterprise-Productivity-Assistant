from unittest.mock import patch

from server.services.mcp.mcp_tool_service import execute_mcp_tool


def test_execute_mcp_tool():
    expected = ["GitHub result"]

    with patch(
        "server.services.mcp.mcp_tool_service.call_mcp_tool",
        return_value=expected,
    ):
        result = execute_mcp_tool("github_list_repositories")

    assert result == expected