from server.services.llm_service import generate_response


def generate_hypothetical_document(question: str) -> str:
    """
    Generate a hypothetical document that could answer the question.
    This document is used for embedding-based retrieval.
    """

    prompt = f"""
Write a hypothetical passage that would directly answer the user's
question.

Rules:
- Write as if the passage came from a knowledge base.
- Include relevant technical concepts and terminology.
- Do not mention that the passage is hypothetical.
- Do not say "I don't know".
- Do not add conversational filler.

User question:
{question}

Hypothetical passage:
"""

    response = generate_response(prompt)

    return response.strip()