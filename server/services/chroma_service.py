import chromadb
from chromadb.config import Settings

# Create a persistent ChromaDB client
chroma_client = chromadb.PersistentClient(
    path="data/chroma_db",
    settings=Settings(anonymized_telemetry=False)
)

# Create or get the collection
collection = chroma_client.get_or_create_collection(
    name="documents"
)

def store_embeddings(chunks, embeddings, filename):
    """
    Store chunks and embeddings in ChromaDB.
    """

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        ids.append(f"{filename}_chunk_{i}")

        documents.append(chunk)

        metadatas.append({
            "filename": filename,
            "chunk": i
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

def get_collection_count():
    """
    Returns the number of stored documents.
    """
    return collection.count()

def search_embeddings(query_embedding, top_k=3):
    """
    Search the most relevant document chunks.
    """

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results