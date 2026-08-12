from fastapi import UploadFile

from server.services.bm25_service import create_bm25_index
from server.services import bm25_store

from server.services.upload_service import save_uploaded_file
from server.services.pdf_service import extract_text_from_pdf
from server.services.text_cleaner import clean_text
from server.services.chunk_service import split_text_into_chunks
from server.services.embedding_service import generate_embeddings
from server.services.chroma_service import (
    store_embeddings,
    get_collection_count,
)
from server.services.parent_child_service import create_parent_child_chunks


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

    # Create parent-child chunks
    parent_child_pairs = create_parent_child_chunks(text)

    # Child chunks are used for retrieval
    child_chunks = [
        item["child"]
        for item in parent_child_pairs
    ]

    # Parent chunks are kept for returning broader context
    parent_chunks = [
        item["parent"]
        for item in parent_child_pairs
    ]

    # Create BM25 index and store in bm25_store
    bm25_store.bm25_index = create_bm25_index(child_chunks)
    bm25_store.document_chunks = child_chunks

    # Generate embeddings
    embeddings = generate_embeddings(child_chunks)

    # Store embeddings in ChromaDB
    store_embeddings(
        chunks=child_chunks,
        embeddings=embeddings,
        filename=file_path.name,
        parent_chunks=parent_chunks,
    )

    # Print total stored chunks
    print(f"Total chunks stored: {get_collection_count()}")

    return { 
    "message": "File uploaded successfully.",
    "filename": file_path.name,
    "file_path": str(file_path),
    "characters": len(text),
    "chunks": len(child_chunks),
    "embedding_count": len(embeddings),
    "embedding_dimension": (
        len(embeddings[0])
        if len(embeddings) > 0
        else 0
    ),
}