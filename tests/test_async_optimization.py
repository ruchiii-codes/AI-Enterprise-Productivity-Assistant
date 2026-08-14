import inspect

from server.services.mcp.mcp_client import call_mcp_tool


def test_mcp_client_is_async():
    assert inspect.iscoroutinefunction(call_mcp_tool)