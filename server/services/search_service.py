from server.services.embedding_service import generate_query_embedding
from server.services.chroma_service import search_embeddings
from server.services.prompt_service import build_prompt


def search_documents(query: str):
    """
    Search relevant documents and build a prompt for the LLM.
    """

    # Generate embedding for the user's question
    query_embedding = generate_query_embedding(query)

    # Search ChromaDB
    results = search_embeddings(query_embedding)

    # Extract useful information
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    filtered_documents = []
    filtered_metadatas = []
    filtered_distances = []

    for document, metadata, distance in zip(documents, metadatas, distances):
        if distance < 0.7:
            filtered_documents.append(document)
            filtered_metadatas.append(metadata)
            filtered_distances.append(distance)

    if not filtered_documents:
        return {
            "prompt": None,
            "documents": [],
            "metadatas": [],
            "distances": []
    }        

    prompt = build_prompt(query, filtered_documents)

    # Build prompt
    prompt = build_prompt(query, documents)

    return {
    "prompt": prompt,
    "documents": filtered_documents,
    "metadatas": filtered_metadatas,
    "distances": filtered_distances
}