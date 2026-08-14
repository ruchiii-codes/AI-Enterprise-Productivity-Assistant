from server.services.llm_service import generate_response
from server.utils.cache import TTLCache


query_rewrite_cache = TTLCache(ttl_seconds=300)


def rewrite_query(question: str) -> str:
    """
    Rewrite a user's question into a clearer search query
    optimized for document retrieval.
    """

    cache_key = f"rewrite:{question.strip().lower()}"

    cached_result = query_rewrite_cache.get(cache_key)

    if cached_result is not None:
        return cached_result

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

    rewritten_query = generate_response(prompt).strip()

    query_rewrite_cache.set(cache_key, rewritten_query)

    return rewritten_query