from typing import List

import numpy as np
from rank_bm25 import BM25Okapi


def create_bm25_index(chunks: List[str]):

    tokenized_chunks = [chunk.split() for chunk in chunks]

    bm25 = BM25Okapi(tokenized_chunks)

    return bm25

def bm25_search(
    query: str,
    bm25: BM25Okapi,
    chunks: List[str],
    metadata: List[dict],
    top_k: int = 3,
    user_id: int | None = None,
    conversation_id: int | None = None,
):
    tokenized_query = query.split()

    scores = bm25.get_scores(tokenized_query)

    allowed_indices = [
        index
        for index, item in enumerate(metadata)
        if (
            user_id is None
            or item.get("user_id") == user_id
        )
        and (
            conversation_id is None
            or item.get("conversation_id") == conversation_id
        )
    ]

    if not allowed_indices:
        return []

    ranked_indices = sorted(
        allowed_indices,
        key=lambda index: scores[index],
        reverse=True,
    )[:top_k]

    return [chunks[index] for index in ranked_indices]