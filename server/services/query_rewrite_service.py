from server.services.llm_service import generate_response


def rewrite_query(question: str) -> str:
    """
    Rewrite a user's question into a clearer search query
    optimized for document retrieval.
    """

    prompt = f"""
Rewrite the following user question into a concise search query
for retrieving relevant information from a knowledge base.

Rules:
- Preserve the original meaning.
- Remove unnecessary conversational wording.
- Keep important keywords.
- Return only the rewritten query.
- Do not answer the question.

User question:
{question}

Rewritten search query:
"""

    rewritten_query = generate_response(prompt)

    return rewritten_query.strip()