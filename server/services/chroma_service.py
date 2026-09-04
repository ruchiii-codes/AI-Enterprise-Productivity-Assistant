import chromadb
from chromadb.config import Settings
import uuid

# Create a persistent ChromaDB client
chroma_client = chromadb.PersistentClient(
    path="data/chroma_db",
    settings=Settings(anonymized_telemetry=False)
)

# Create or get the collection
collection = chroma_client.get_or_create_collection(
    name="documents"
)

def store_embeddings(
    chunks,
    embeddings,
    filename,
    parent_chunks=None,
    user_id=None,
    conversation_id=None,
):
    """
    Store child chunks and their parent chunks in ChromaDB.
    """
    print(
        "DEBUG CHROMA:",
        "user_id =", user_id,
        "| conversation_id =", conversation_id,
        "| filename =", filename,
    )

    ids = []
    documents = []
    metadatas = []

    document_id = str(uuid.uuid4())

    for i, chunk in enumerate(chunks):
        ids.append(f"{document_id}_child_{i}")
        documents.append(chunk)

        parent = (
            parent_chunks[i]
            if parent_chunks is not None
            else chunk
        )

        metadatas.append({
            "filename": filename,
            "chunk": i,
            "parent_id": i,
            "parent": parent,
            "user_id": user_id,
            "conversation_id": conversation_id,
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
    )

def get_collection_count():
    """
    Returns the number of stored documents.
    """
    return collection.count()

def search_embeddings(
    query_embedding,
    top_k=3,
    user_id=None,
    conversation_id=None,
):
    """
    Search the most relevant document chunks.
    """

    query_kwargs = {
        "query_embeddings": [query_embedding.tolist()],
        "n_results": top_k,
    }
    
    if user_id is not None and conversation_id is not None:
        query_kwargs["where"] = {
            "$and": [
                {"user_id": user_id},
                {"conversation_id": conversation_id},
            ]
        }
    
    results = collection.query(**query_kwargs)

    return results

def get_parent_documents(results):
    """
    Replace retrieved child chunks with their parent documents.
    """

    if not results or not results.get("documents"):
        return results

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    parent_documents = []
    parent_metadatas = []

    seen_parents = set()

    for document, metadata in zip(documents, metadatas):
        parent_id = metadata.get("parent_id")

        if parent_id in seen_parents:
            continue

        seen_parents.add(parent_id)

        parent_documents.append(
            metadata.get("parent", document)
        )

        parent_metadatas.append(metadata)

    results["documents"][0] = parent_documents
    results["metadatas"][0] = parent_metadatas

    return results
