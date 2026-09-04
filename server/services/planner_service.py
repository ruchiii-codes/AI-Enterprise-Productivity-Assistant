from enum import Enum
import logging

from server.services.llm_service import classify_query

logger = logging.getLogger(__name__)


class Route(Enum):
    RETRIEVAL = "retrieval"
    SUMMARIZATION = "summarization"
    DIRECT_LLM = "direct_llm"
    TOOL = "tool"


def plan_route(
    query: str,
    history=None,
    has_uploaded_documents: bool = False,
) -> dict:
    """
    Generate a structured execution plan using the LLM classifier.

    Returns:
        {
            "route": Route,
            "tool": str | None,
            "intent": str | None,
            "parameters": dict
        }

    The LLM remains responsible for understanding the user's
    natural-language intent. This function only normalizes the result.
    """

    try:
        result = classify_query(
            query=query,
            history=history,
            has_uploaded_documents=has_uploaded_documents,
        )

        route_value = result.get("route")

        if route_value == "retrieval":
            route = Route.RETRIEVAL

        elif route_value == "summarization":
            route = Route.SUMMARIZATION

        elif route_value == "tool":
            route = Route.TOOL

        elif route_value == "direct_llm":
            route = Route.DIRECT_LLM

        else:
            logger.warning(
                "Unknown route returned by classifier: %s",
                route_value,
            )
            route = Route.DIRECT_LLM

        return {
            "route": route,
            "tool": result.get("tool"),
            "intent": result.get("intent"),
            "parameters": result.get("parameters", {}),
        }

    except Exception as e:
        logger.exception(
            "Intelligent routing failed. Falling back to DIRECT_LLM: %s",
            e,
        )

        return {
            "route": Route.DIRECT_LLM,
            "tool": None,
            "intent": None,
            "parameters": {},
        }