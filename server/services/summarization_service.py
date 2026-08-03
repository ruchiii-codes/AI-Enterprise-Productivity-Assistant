import os

from server.services.pdf_service import extract_text_from_pdf
from server.services.llm_service import generate_response

from server.services.retriever_agent import retrieve


UPLOAD_FOLDER = "data/uploads"


def summarize_latest_pdf():
    """
    Summarizes the most recently uploaded PDF.
    """

    pdf_files = [
        f for f in os.listdir(UPLOAD_FOLDER)
        if f.endswith(".pdf")
    ]

    if not pdf_files:
        return None

    latest_pdf = max(
        pdf_files,
        key=lambda f: os.path.getmtime(
            os.path.join(UPLOAD_FOLDER, f)
        )
    )

    pdf_path = os.path.join(
        UPLOAD_FOLDER,
        latest_pdf,
    )

    document_text = extract_text_from_pdf(pdf_path)

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


def summarize_topic(question: str):
    """
    Summarize only the relevant part of the document.
    """

    results = retrieve(question)

    if results["prompt"] is None:
        return None

    prompt = f"""
You are an AI assistant.

Summarize the following information.

{results["prompt"]}
"""

    return generate_response(prompt)


def summarize(question: str):
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
        return summarize_latest_pdf()

    # Topic summary
    return summarize_topic(question)    