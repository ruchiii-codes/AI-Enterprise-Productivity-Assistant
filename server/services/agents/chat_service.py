"""Chat orchestration.

Drives a single chat turn: plan the route, run the orchestrator, persist the
exchange, and generate the reply. This was previously inline in main.py.

HTTPException is raised directly rather than through a separate domain-error
hierarchy, so that status codes and detail strings stay byte-identical to the
previous implementation.
"""

import logging

from fastapi import HTTPException
from openai import APIConnectionError, APIError, APITimeoutError
from sqlalchemy.orm import Session

from server.db.models import Document, User
from server.schemas.chat import ChatRequest
from server.services.agents.orchestrator_service import execute
from server.services.agents.planner_service import Route, plan_route
from server.services.agents.prompt_builder import build_messages
from server.services.conversations.conversation_service import (
    get_conversation,
    update_conversation_title,
)
from server.services.conversations.message_service import (
    add_message,
    get_recent_messages,
)
from server.services.providers.llm_service import (
    format_tool_response,
    generate_response,
)

logger = logging.getLogger(__name__)

# Sent when the retrieval route has already gathered document context.
RETRIEVAL_SYSTEM_PROMPT = (
    "You are answering a question about an uploaded document. "
    "Use ONLY the document context contained in the user message. "
    "If the answer is present in that context, answer it directly. "
    "Do not claim the answer is missing when relevant information "
    "is present. Do not use outside knowledge."
)


def handle_chat(
    db: Session,
    current_user: User,
    chat_request: ChatRequest,
) -> dict:
    """Process one chat turn and return {"answer": str, "sources": list}."""

    logger.info("Authenticated request from user: %s", current_user.email)

    conversation = get_conversation(
        db=db,
        conversation_id=chat_request.conversation_id,
        user_id=current_user.id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    # Validate user input
    if not chat_request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    history = get_recent_messages(
        db=db,
        conversation_id=chat_request.conversation_id,
    )

    has_uploaded_documents = (
        db.query(Document)
        .filter(
            Document.user_id == current_user.id,
            Document.conversation_id == chat_request.conversation_id,
        )
        .first()
        is not None
    )

    logger.info(
        "Conversation %s has uploaded documents: %s",
        chat_request.conversation_id,
        has_uploaded_documents,
    )

    plan = plan_route(
        chat_request.question,
        history=history,
        has_uploaded_documents=has_uploaded_documents,
    )

    results = {
        "metadatas": []
    }

    route = plan["route"]

    logger.info(
        "Planner decision: route=%s tool=%s intent=%s parameters=%s",
        route.value,
        plan.get("tool"),
        plan.get("intent"),
        plan.get("parameters"),
    )

    # -----------------------------
    # Orchestrator
    # -----------------------------
    if route != Route.DIRECT_LLM:

        result = execute(
            plan=plan,
            question=chat_request.question,
            history=history,
            user_id=current_user.id,
            conversation_id=chat_request.conversation_id,
        )

        logger.info(
            "RETRIEVAL RESULT: prompt_is_none=%s, prompt_type=%s, keys=%s",
            result.get("prompt") is None if isinstance(result, dict) else "NOT_DICT",
            type(result.get("prompt")).__name__ if isinstance(result, dict) else "N/A",
            list(result.keys()) if isinstance(result, dict) else "N/A",
        )

        # Retrieval continues into chat flow
        if route == Route.RETRIEVAL:

            if result["prompt"] is None:
                return {
                    "answer": "I couldn't find any relevant information in the uploaded documents.",
                    "sources": [],
                }

            prompt = result["prompt"]
            results = {
                "metadatas": result["metadatas"],
            }

        # Tool & Summarization
        else:
            add_message(
                db=db,
                conversation_id=chat_request.conversation_id,
                role="user",
                content=chat_request.question,
            )

            answer = result["answer"]

            if route == Route.TOOL:
                answer = format_tool_response(
                    tool=plan.get("tool"),
                    intent=plan.get("intent"),
                    result=answer,
                    question=chat_request.question,
                )

            add_message(
                db=db,
                conversation_id=chat_request.conversation_id,
                role="assistant",
                content=answer,
            )

            if conversation.title == "New Conversation":
                update_conversation_title(
                    db=db,
                    conversation_id=chat_request.conversation_id,
                    user_id=current_user.id,
                    title=chat_request.question[:60],
                )

            return {
                "answer": answer,
                "sources": result.get("sources", []),
            }

    # -----------------------------
    # Direct LLM
    # -----------------------------
    else:

        prompt = chat_request.question

        results = {
            "metadatas": [],
        }

    # Build messages for the LLM
    if route == Route.RETRIEVAL:
        # RAG already retrieved the document context.
        # Send the grounded prompt explicitly to the LLM.
        messages = [
            {
                "role": "system",
                "content": RETRIEVAL_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]
    else:
        # Direct LLM requests can use conversation history
        history = get_recent_messages(
            db=db,
            conversation_id=chat_request.conversation_id,
        )

        messages = build_messages(
            history=history,
            current_prompt=prompt,
        )

    add_message(
        db=db,
        conversation_id=chat_request.conversation_id,
        role="user",
        content=chat_request.question,
    )

    # Generate AI response
    try:
        answer = generate_response(messages)

        add_message(
            db=db,
            conversation_id=chat_request.conversation_id,
            role="assistant",
            content=answer,
            sources=results["metadatas"],
        )

        # Set conversation title from the first user message
        if conversation.title == "New Conversation":
            update_conversation_title(
                db=db,
                conversation_id=chat_request.conversation_id,
                user_id=current_user.id,
                title=chat_request.question[:60],
            )
    except APIConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to the AI service."
        )

    except APITimeoutError:
        raise HTTPException(
            status_code=503,
            detail="The AI service took too long to respond."
        )

    except APIError:
        raise HTTPException(
            status_code=503,
            detail="The AI service is currently unavailable."
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected server error occurred."
        )

    return {
        "answer": answer,
        "sources": results["metadatas"] if results else []
    }
