from server.services.planner_service import Route
from server.services.retriever_agent import retrieve
from server.services.summarization_service import summarize
from server.services.tool_service import count_uploaded_pdfs

from server.services.multi_tool.tool_selector import select_tools
from server.services.multi_tool.multi_tool_executor import execute_multiple_tools
from server.services.multi_tool.result_formatter import format_multi_tool_results


def execute(route: Route, question: str):

    if route == Route.RETRIEVAL:
        return retrieve(question)

    elif route == Route.SUMMARIZATION:

        summary = summarize(question)

        if summary is None:
            return {
                "answer": "No relevant information found.",
                "sources": [],
            }

        return {
            "answer": summary,
            "sources": [],
        }

    elif route == Route.TOOL:

        from server.services.tool_router import resolve_tool

        selected_tools = select_tools(question)

        # No multi-tool match → keep existing behavior
        if len(selected_tools) <= 1:
            result = resolve_tool(question)

            return {
                "answer": result,
                "sources": [],
            }

        # Multiple tools detected
        results = execute_multiple_tools(selected_tools)

        formatted_results = format_multi_tool_results(results)

        return {
            "answer": formatted_results,
            "sources": [],
        }

    return None