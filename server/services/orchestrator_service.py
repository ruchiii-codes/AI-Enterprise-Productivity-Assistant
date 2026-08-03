from server.services.planner_service import Route
from server.services.retriever_agent import retrieve
from server.services.summarization_service import summarize
from server.services.tool_service import count_uploaded_pdfs


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

        total = count_uploaded_pdfs()

        return {
            "answer": f"You have uploaded {total} PDF(s).",
            "sources": [],
        }

    return None