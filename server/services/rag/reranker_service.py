import logging
from typing import List

from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

def rerank_documents(
    query: str,
    documents: List[str],
    top_k: int = 3,
    min_score: float = 0.1,
):
    pairs = [
        (query, document)
        for document in documents
    ]

    scores = reranker.predict(pairs)

    scored_documents = list(zip(documents, scores))

    if len(scores):
        logger.debug(
            "Reranked %d documents (score %.3f to %.3f)",
            len(scored_documents),
            float(min(scores)),
            float(max(scores)),
        )

    scored_documents.sort(
        key=lambda x: x[1],
        reverse=True,
    )

    filtered_documents = [
        document
        for document, score in scored_documents
        if score >= min_score
    ]

    return filtered_documents[:top_k]
