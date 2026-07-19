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