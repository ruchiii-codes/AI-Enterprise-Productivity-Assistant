import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mcp.server import MCPServer

from server.services.integrations.calendar.calendar_service import (
    get_upcoming_events,
)

from server.services.integrations.gmail.gmail_service import list_messages

from server.services.integrations.github.github_service import list_repositories


mcp = MCPServer("Enterprise Productivity Assistant")


@mcp.tool()
def ping() -> str:
    """Check whether the MCP server is running."""
    return "pong"


@mcp.tool()
def calendar_get_upcoming_events() -> str:
    """Get the user's upcoming Google Calendar events."""
    events = get_upcoming_events(max_results=10)

    if not events:
        return "No upcoming calendar events found."

    results = []

    for event in events:
        start = event.get("start", {}).get("dateTime")
        end = event.get("end", {}).get("dateTime")
        summary = event.get("summary", "Untitled event")

        results.append(
            f"Title: {summary}\n"
            f"Start: {start}\n"
            f"End: {end}"
        )

    return "\n\n".join(results)


@mcp.tool()
def gmail_list_messages() -> str:
    """Get the user's latest Gmail messages."""
    messages = list_messages(max_results=10)

    if not messages:
        return "No Gmail messages found."

    results = []

    for index, message in enumerate(messages, start=1):
        results.append(
            f"{index}. {message.get('subject', 'No subject')}\n"
            f"From: {message.get('from', 'Unknown')}\n"
            f"Date: {message.get('date', 'Unknown')}\n"
            f"Snippet: {message.get('snippet', '')}"
        )

    return "\n\n".join(results)


@mcp.tool()
def github_list_repositories() -> str:
    """List repositories owned by the authenticated GitHub user."""
    repositories = list_repositories()

    if not repositories:
        return "No GitHub repositories found."

    results = []

    for index, repo in enumerate(repositories, start=1):
        visibility = "Private" if repo.get("private") else "Public"

        results.append(
            f"{index}. {repo.get('name', 'Unnamed repository')}\n"
            f"Visibility: {visibility}\n"
            f"URL: {repo.get('html_url', '')}"
        )

    return "\n\n".join(results)

if __name__ == "__main__":
    mcp.run()    