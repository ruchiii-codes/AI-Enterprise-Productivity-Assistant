from typing import List

from sentence_transformers import CrossEncoder

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

    print("\n" + "=" * 80)
    print("RERANKER SCORES")
    print("=" * 80)

    for document, score in scored_documents:
        print("SCORE:", score)
        print("DOCUMENT:", document[:300])
        print("-" * 80)

    print("=" * 80 + "\n")

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