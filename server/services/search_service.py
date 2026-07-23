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

    # Build prompt
    prompt = build_prompt(query, documents)

    return {
        "prompt": prompt,
        "documents": documents,
        "metadatas": metadatas,
        "distances": distances
    }