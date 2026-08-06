from enum import Enum


class Route(Enum):

    RETRIEVAL = "retrieval"

    SUMMARIZATION = "summarization"

    DIRECT_LLM = "direct_llm"

    TOOL = "tool"


def plan_route(query: str) -> Route:

    query = query.lower().strip()

    words = query.split()

    # -----------------------------
    # Greetings
    # -----------------------------
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

    # -----------------------------
    # Conversation / Memory
    # -----------------------------
    if any(
        phrase in query
        for phrase in [
            "my name is",
            "i am",
            "i'm",
            "my favorite",
            "remember",
            "don't forget",
            "keep in mind",
            "i like",
            "i love",
            "i prefer",
            "i work",
            "i study",
            "i live",
        ]
    ):
        return Route.DIRECT_LLM

    # -----------------------------
    # Follow-up questions
    # -----------------------------
    if any(
        phrase in query
        for phrase in [
            "explain it",
            "explain this",
            "tell me more",
            "more details",
            "continue",
            "what do you mean",
            "in simple words",
            "simplify",
            "elaborate",
            "give an example",
        ]
    ):
        return Route.DIRECT_LLM

    # -----------------------------
    # Summarization
    # -----------------------------
    if any(
        word in query
        for word in [
            "summarize",
            "summary",
            "summarise",
        ]
    ):
        return Route.SUMMARIZATION

    # -----------------------------
    # Tool
    # -----------------------------
    if any(
        word in query
        for word in [
            "how many pdf",
            "number of pdf",
            "uploaded pdf",
        ]
    ):
        return Route.TOOL

    # -----------------------------
    # Memory Recall Questions
    # -----------------------------
    if any(
        phrase in query
        for phrase in [
            "what is my",
            "what's my",
            "who am i",
            "what did i",
            "do you remember",
            "what was my",
            "tell me my",
        ]
    ):
        return Route.DIRECT_LLM    

    # -----------------------------
    # Retrieval
    # -----------------------------
    retrieval_keywords = [
        "what is",
        "what are",
        "define",
        "definition",
        "explain",
        "bm25",
        "hybrid search",
        "rag",
        "embedding",
        "vector",
        "document",
        "pdf",
    ]

    if any(keyword in query for keyword in retrieval_keywords):
        return Route.RETRIEVAL

    # -----------------------------
    # Default
    # -----------------------------
    return Route.DIRECT_LLM