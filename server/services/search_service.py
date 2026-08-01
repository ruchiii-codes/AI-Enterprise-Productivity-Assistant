from server.services.embedding_service import generate_query_embedding
from server.services.chroma_service import search_embeddings
from server.services.prompt_service import build_prompt

from server.services.bm25_service import bm25_search
from server.services import bm25_store
from server.services.reranker_service import rerank_documents


def search_documents(query: str):
    """
    Search relevant documents and build a prompt for the LLM.
    """

    # Generate embedding
    query_embedding = generate_query_embedding(query)

    # Semantic Search
    results = search_embeddings(query_embedding)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    filtered_documents = []
    filtered_metadatas = []
    filtered_distances = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        if distance < 0.7:
            filtered_documents.append(document)
            filtered_metadatas.append(metadata)
            filtered_distances.append(distance)

    if not filtered_documents:
        return {
            "prompt": None,
            "documents": [],
            "metadatas": [],
            "distances": [],
        }

    # Default (semantic only)
    final_documents = filtered_documents

    # Hybrid Search
    if bm25_store.bm25_index is not None:

        bm25_results = bm25_search(
            query=query,
            bm25=bm25_store.bm25_index,
            chunks=bm25_store.document_chunks,
            top_k=3,
        )

        hybrid_documents = list(
            dict.fromkeys(filtered_documents + bm25_results)
        )

        final_documents = rerank_documents(
            query=query,
            documents=hybrid_documents,
            top_k=3,
        )

    prompt = build_prompt(
        query,
        final_documents,
    )

    return {
        "prompt": prompt,
        "documents": final_documents,
        "metadatas": filtered_metadatas,
        "distances": filtered_distances,
    }