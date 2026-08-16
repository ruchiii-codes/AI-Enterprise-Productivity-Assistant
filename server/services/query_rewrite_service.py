from server.services.llm_service import generate_response
from server.utils.cache import TTLCache


query_rewrite_cache = TTLCache(ttl_seconds=300)


def rewrite_query(question: str, history=None) -> str:
    """
    Rewrite a user's question into a clearer search query
    optimized for document retrieval.
    """

    cache_key = f"rewrite:{question.strip().lower()}"

    cached_result = query_rewrite_cache.get(cache_key)

    if cached_result is not None:
        return cached_result

    history_text = ""
    
    if history:
        history_text = "\n".join(
            f"{message.role}: {message.content}"
            for message in history[-6:]
        )
    
    prompt = f"""
    Rewrite the following user question into a concise, standalone search query
    for retrieving relevant information from a knowledge base.
    
    Use the conversation history to resolve references such as:
    - it
    - this
    - that
    - they
    - these
    - the above
    - previous answer
    
    Rules:
    - Preserve the original meaning.
    - Resolve ambiguous references using the conversation history.
    - If the current question is already standalone, keep its meaning unchanged.
    - Keep important project/document keywords.
    - Return only the rewritten search query.
    - Do not answer the question.
    
    Conversation history:
    {history_text}
    
    Current user question:
    {question}
    
    Rewritten search query:
    """

    rewritten_query = generate_response(prompt).strip()

    query_rewrite_cache.set(cache_key, rewritten_query)

    return rewritten_query