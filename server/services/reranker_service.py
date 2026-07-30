from typing import List

from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

def rerank_documents(
    query: str,
    documents: List[str],
    top_k: int = 3,
):
    pairs = [
        (query, document)
        for document in documents
    ]

    scores = reranker.predict(pairs)

    scored_documents = list(zip(documents, scores))

    scored_documents.sort(
        key=lambda x: x[1],
        reverse=True
    )

    top_documents = scored_documents[:top_k]

    return [
        document
        for document, score in top_documents
    ]