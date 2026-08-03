from enum import Enum


class Route(Enum):

    RETRIEVAL = "retrieval"

    SUMMARIZATION = "summarization"

    DIRECT_LLM = "direct_llm"

    TOOL = "tool"


def plan_route(query: str) -> Route:

    query = query.lower()

    # Direct LLM

    words = query.split()

    if any(
        greeting in words
        for greeting in [
            "hi",
            "hello",
            "hey",
        ]
    ):
        return Route.DIRECT_LLM

    if any(
        phrase in query
        for phrase in [
            "good morning",
            "good afternoon",
            "good evening",
        ]
    ):
        return Route.DIRECT_LLM

    # Summarization
    if any(
        word in query
        for word in [
            "summarize",
            "summary",
            "summarise",
        ]
    ):
        return Route.SUMMARIZATION

    # Tool
    if any(
        word in query
        for word in [
            "how many pdf",
            "number of pdf",
            "uploaded pdf",
        ]
    ):
        return Route.TOOL

    # Follow-up questions
    if any(
        phrase in query
        for phrase in [
            "explain it",
            "explain this",
            "tell me more",
            "more details",
            "in simple words",
            "simplify",
            "elaborate",
            "why",
            "how",
        ]
    ):
        return Route.DIRECT_LLM

    # Default
    return Route.RETRIEVAL
    