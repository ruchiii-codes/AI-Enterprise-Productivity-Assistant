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
    top_k: int = 3,
):

    tokenized_query = query.split()

    scores = bm25.get_scores(tokenized_query)

    top_indices = np.argsort(scores)[::-1][:top_k]

    top_chunks = [chunks[i] for i in top_indices]

    return top_chunks