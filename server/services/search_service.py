from server.services.embedding_service import generate_query_embedding
from server.services.chroma_service import (
    search_embeddings,
    get_parent_documents,
)
from server.services.prompt_service import build_prompt

from server.services.bm25_service import bm25_search
from server.services import bm25_store
from server.services.reranker_service import rerank_documents
from server.services.query_rewrite_service import rewrite_query
from server.services.multi_query_service import generate_multi_queries
from server.services.hyde_service import generate_hypothetical_document
from server.services.context_compression_service import compress_context

def search_documents(
    query: str,
    history=None,
    user_id: int | None = None,
    conversation_id: int | None = None,
):
    """
    Search relevant documents and build a prompt for the LLM.
    """

    # Rewrite query for better retrieval
    rewritten_query = rewrite_query(
        query,
        history=history,
    )    
    multi_queries = generate_multi_queries(rewritten_query)
    hypothetical_document = generate_hypothetical_document(rewritten_query)
   
    # Generate embedding from rewritten query
    all_documents = []
    all_metadatas = []
    all_distances = []

    for search_query in multi_queries:
        query_embedding = generate_query_embedding(search_query)

        results = search_embeddings(
            query_embedding,
            user_id=user_id,
            conversation_id=conversation_id,
        )

        results = get_parent_documents(results)

        all_documents.extend(results["documents"][0])
        all_metadatas.extend(results["metadatas"][0])
        all_distances.extend(results["distances"][0])

        
    # HyDE retrieval
    hyde_embedding = generate_query_embedding(hypothetical_document)

    hyde_results = search_embeddings(
        hyde_embedding,
        user_id=user_id,
        conversation_id=conversation_id,
    )

    hyde_results = get_parent_documents(hyde_results)

    all_documents.extend(hyde_results["documents"][0])
    all_metadatas.extend(hyde_results["metadatas"][0])
    all_distances.extend(hyde_results["distances"][0])

    # Remove duplicate documents
    unique_results = {}

    for document, metadata, distance in zip(
        all_documents,
        all_metadatas,
        all_distances,
    ):
        if document not in unique_results:
            unique_results[document] = (metadata, distance)

    documents = list(unique_results.keys())
    metadatas = [item[0] for item in unique_results.values()]
    distances = [item[1] for item in unique_results.values()]

    print("\n" + "=" * 80)
    print("RETRIEVAL DISTANCES")
    print("=" * 80)
    
    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        print("DISTANCE:", distance)
        print("FILENAME:", metadata.get("filename"))
        print("DOCUMENT:", document[:200])
        print("-" * 80)
    
    print("=" * 80 + "\n")

    filtered_documents = []
    filtered_metadatas = []
    filtered_distances = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        if distance < 1.8:
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

    print("\n" + "=" * 80)
    print("AFTER DISTANCE FILTER")
    print("=" * 80)
    for doc in final_documents:
        print(doc[:500])
    print("=" * 80)

    # Hybrid Search
    if bm25_store.bm25_index is not None:
    
        bm25_results = bm25_search(
            query=rewritten_query,
            bm25=bm25_store.bm25_index,
            chunks=bm25_store.document_chunks,
            metadata=bm25_store.document_metadata,
            top_k=3,
            user_id=user_id,
            conversation_id=conversation_id,
        )
    
        hybrid_documents = list(
            dict.fromkeys(filtered_documents + bm25_results)
        )
    
        final_documents = rerank_documents(
            query=rewritten_query,
            documents=hybrid_documents,
            top_k=3,
            min_score=0.1,
        )
    
        # Keep metadata aligned with the final reranked documents
        metadata_by_document = {
            document: metadata
            for document, metadata in zip(
                filtered_documents,
                filtered_metadatas,
            )
        }
    
        final_metadatas = [
            metadata_by_document[document]
            for document in final_documents
            if document in metadata_by_document
        ]
    
    else:
        final_metadatas = filtered_metadatas

        print("\n" + "=" * 80)
        print("AFTER RERANKING")
        print("=" * 80)
        for doc in final_documents:
            print(doc[:500])
        print("=" * 80)

    # Use the actual retrieved documents as context.
    # Do not rewrite/compress them with an LLM here,
    # because that can introduce information not present
    # in the uploaded documents.
    
    retrieved_context = "\n\n---\n\n".join(final_documents)
    
    if not retrieved_context.strip():
        return {
            "prompt": None,
            "documents": [],
            "metadatas": [],
            "distances": [],
        }
    
    print("\n" + "=" * 80)
    print("FINAL RETRIEVED CONTEXT")
    print("=" * 80)
    print(retrieved_context)
    print("=" * 80 + "\n")
    
    prompt = build_prompt(
        query,
        [retrieved_context],
    )

    return {
        "prompt": prompt,
        "documents": final_documents,
        "metadatas": final_metadatas,
        "distances": [],
    }