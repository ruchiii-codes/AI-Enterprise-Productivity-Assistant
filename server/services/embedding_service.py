from sentence_transformers import SentenceTransformer

# Load the embedding model only once
embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def generate_embeddings(chunks: list[str]):
    """
    Generate embeddings for a list of text chunks.
    """

    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True
    )

    return embeddings


def generate_query_embedding(query: str):
    """
    Generate an embedding for a user's search query.
    """

    embedding = embedding_model.encode(
        query,
        convert_to_numpy=True
    )

    return embedding