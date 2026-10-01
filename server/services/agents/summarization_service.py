from pathlib import Path

from server.config import settings
from server.db.base import SessionLocal
from server.db.models import Document
from server.services.agents.retriever_agent import retrieve
from server.services.providers.llm_service import generate_response
from server.services.rag.pdf_service import extract_text_from_pdf


def summarize_latest_pdf(user_id=None, conversation_id=None):
    """
    Summarize the caller's most recently uploaded PDF.
    """

    # Without an owner there is no safe document to pick. The directory scan
    # this replaces took whichever PDF was newest on disk, which in a
    # multi-user deployment is usually somebody else's.
    if user_id is None:
        return None

    db = SessionLocal()

    try:
        query = db.query(Document).filter(Document.user_id == user_id)

        # Scoped to the conversation when there is one, so "summarize this
        # pdf" means the one in this chat -- the scoping retrieval uses too.
        if conversation_id is not None:
            query = query.filter(
                Document.conversation_id == conversation_id
            )

        document = (
            query
            .order_by(Document.id.desc())
            .first()
        )
    finally:
        db.close()

    if document is None:
        return None

    pdf_path = Path(document.file_path)

    # Rows written on another machine hold a path that does not resolve here,
    # so fall back to the stored file's name in the current upload directory.
    if not pdf_path.exists():
        pdf_path = settings.UPLOAD_DIR / pdf_path.name

    # Never read outside the upload directory, whatever the row says.
    if pdf_path.resolve().parent != settings.UPLOAD_DIR.resolve():
        return None

    if not pdf_path.exists():
        return None

    document_text = extract_text_from_pdf(str(pdf_path))

    prompt = f"""
You are an AI assistant.

Summarize the following document.

Your summary should include:

1. Main topic
2. Important concepts
3. Key takeaways

Document:

{document_text}
"""

    return generate_response(prompt)


def summarize_topic(question: str, user_id=None, conversation_id=None):
    """
    Summarize only the relevant part of the document.
    """

    results = retrieve(
        question,
        user_id=user_id,
        conversation_id=conversation_id,
    )

    if results["prompt"] is None:
        return None

    prompt = f"""
You are an AI assistant.

Summarize the following information.

{results["prompt"]}
"""

    return generate_response(prompt)


def summarize_gmail_message(message: dict):
    """
    Summarizes a Gmail message.
    """

    subject = message.get("subject") or "No Subject"
    sender = message.get("from") or "Unknown"
    body = message.get("body") or ""

    if not body.strip():
        return None

    prompt = f"""
You are an AI assistant.

Summarize the following email.

Include:
1. Main purpose
2. Important points
3. Required action, if any
4. Key dates or deadlines, if mentioned

Email:

From: {sender}
Subject: {subject}

{body}
"""

    return generate_response(prompt)


def summarize(question: str, user_id=None, conversation_id=None):
    """
    Smart Summarizer Agent.
    """

    query = question.lower()

    # Entire PDF
    if (
        "this pdf" in query
        or "the pdf" in query
        or "entire pdf" in query
    ):
        return summarize_latest_pdf(
            user_id=user_id,
            conversation_id=conversation_id,
        )

    # Topic summary
    return summarize_topic(
        question,
        user_id=user_id,
        conversation_id=conversation_id,
    )
