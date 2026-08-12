from server.services.llm_service import generate_response


def generate_multi_queries(question: str, num_queries: int = 3) -> list[str]:
    """
    Generate multiple search queries from a user's question.
    """

    prompt = f"""
Generate {num_queries} different search queries for retrieving
relevant information from a knowledge base.

Rules:
- Preserve the meaning of the original question.
- Each query should use different wording.
- Focus on important concepts and keywords.
- Return exactly one query per line.
- Do not number the queries.
- Do not answer the question.

Original question:
{question}

Search queries:
"""

    response = generate_response(prompt)

    queries = [
        line.strip()
        for line in response.splitlines()
        if line.strip()
    ]

    return queries[:num_queries]