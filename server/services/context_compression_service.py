from server.services.llm_service import generate_response


def compress_context(
    question: str,
    documents: list[str],
) -> str:
    """
    Compress retrieved documents while preserving information
    relevant to the user's question.
    """

    context = "\n\n".join(documents)

    prompt = f"""
You are a context compression system.

Extract only the information from the provided context that is
relevant to answering the user's question.

Rules:
- Preserve important facts, technical details, names, numbers,
  and relationships.
- Remove irrelevant information and repetition.
- Do not invent information.
- Do not answer the question directly.
- Return only the compressed context.

Question:
{question}

Context:
{context}

Compressed context:
"""

    response = generate_response(prompt)

    return response.strip()