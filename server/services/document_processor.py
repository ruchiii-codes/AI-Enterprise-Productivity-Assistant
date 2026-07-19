from fastapi import UploadFile

from server.services.upload_service import save_uploaded_file
from server.services.pdf_service import extract_text_from_pdf
from server.services.text_cleaner import clean_text
from server.services.chunk_service import split_text_into_chunks
from server.services.embedding_service import generate_embeddings
from server.services.chroma_service import (
    store_embeddings,
    get_collection_count,
)


def process_document(file: UploadFile):
    """
    Complete document processing pipeline.
    """

    # Save PDF
    file_path = save_uploaded_file(file)

    # Extract text
    text = extract_text_from_pdf(str(file_path))

    # Clean text
    text = clean_text(text)

    # Split into chunks
    chunks = split_text_into_chunks(text)

    # Generate embeddings
    embeddings = generate_embeddings(chunks)

    # Store embeddings in ChromaDB
    store_embeddings(
        chunks=chunks,
        embeddings=embeddings,
        filename=file_path.name
    )

    # Print total stored chunks
    print(f"Total chunks stored: {get_collection_count()}")

    return {
        "message": "File uploaded successfully.",
        "filename": file_path.name,
        "characters": len(text),
        "chunks": len(chunks),
        "embedding_count": len(embeddings),
        "embedding_dimension": len(embeddings[0]) if len(embeddings) > 0 else 0
    }