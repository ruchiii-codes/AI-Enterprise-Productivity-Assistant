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
    # Gmail Summarization
    # -----------------------------
    if any(
        phrase in query
        for phrase in [
            "summarize my latest email",
            "summarize latest email",
            "summarize my latest mail",
            "summarize latest mail",
            "summarize my email",
            "summarize my emails",
            "summarize email",
            "summarize emails",
        ]
    ):
        return Route.TOOL


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
    # GitHub Tool
    # -----------------------------
    if any(
        phrase in query
        for phrase in [
            "github",
            "repository",
            "repositories",
            "repo",
            "repos",
            "pull request",
            "pull requests",
            "issue",
            "issues",
        ]
    ):
        return Route.TOOL     

    # -----------------------------
    # Gmail Tool
    # -----------------------------
    if any(
        phrase in query
        for phrase in [
            "gmail",
            "email",
            "emails",
            "mail",
            "mails",
            "inbox",
            "send email",
            "send mail",
            "summarize email",
            "summarize emails",
            "summarize my email",
            "summarize my emails",
            "summarize latest email",
            "summarize my latest email",
        ]
    ):
        return Route.TOOL    
    
    # -----------------------------
    # Calendar Tool
    # -----------------------------
    if any(
        phrase in query
        for phrase in [
            "calendar",
            "upcoming events",
            "upcoming meetings",
            "upcoming appointments",
            "show my calendar",
            "show my upcoming meetings",
            "show my upcoming events",
            "find my meeting",
            "find my meetings",
            "find my event",
            "find my events",
            "find meeting",
            "find event",
            "search my calendar",
            "search calendar",
            "schedule a meeting",
            "schedule an event",
            "create a meeting",
            "create an event",
        ]
    ) or (
        "find" in query
        and any(
            word in query
            for word in [
                "meeting",
                "meetings",
                "event",
                "events",
                "interview",
                "appointment",
                "appointments",
            ]
        )
    ):
        return Route.TOOL

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