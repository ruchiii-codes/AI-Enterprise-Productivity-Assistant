"""Retrieval must not lose a good semantic match to the reranker's floor.

rerank_documents drops anything scoring below min_score, and the cross-encoder
returns unbounded logits rather than probabilities: a correctly retrieved
document was measured at -11.0, far below the 0.1 floor. When that empties the
list, search_documents used to build an empty context and return prompt=None,
which the chat service reports as "I couldn't find any relevant information"
even though the answer is in the store.

Everything external is stubbed, so these tests make no network call and load no
model.
"""

import copy

import pytest

from server.services.rag import bm25_store, search_service

ANSWER = "Zephyr Industries reported quarterly revenue of 4.7 million rupees."

CHROMA_RESULT = {
    "documents": [[ANSWER]],
    "metadatas": [[
        {
            "parent_id": 0,
            "parent": ANSWER,
            "filename": "report.pdf",
            "user_id": 7,
            "conversation_id": 3,
        }
    ]],
    "distances": [[0.81]],
}


@pytest.fixture
def retrieval_stubs(monkeypatch):
    """Drive search_documents from canned values, with no models or network."""

    # Query expansion would otherwise call the LLM.
    monkeypatch.setattr(search_service, "rewrite_query", lambda query, history=None: query)
    monkeypatch.setattr(search_service, "generate_multi_queries", lambda query: [query])
    monkeypatch.setattr(
        search_service, "generate_hypothetical_document", lambda query: query
    )
    monkeypatch.setattr(search_service, "generate_query_embedding", lambda query: object())

    # A fresh copy per call: get_parent_documents mutates the result in place,
    # and search_documents queries once per expanded query plus once for HyDE.
    monkeypatch.setattr(
        search_service,
        "search_embeddings",
        lambda *args, **kwargs: copy.deepcopy(CHROMA_RESULT),
    )

    # Hybrid search is only reached when a BM25 index exists, which is the
    # state after any upload.
    monkeypatch.setattr(bm25_store, "bm25_index", object())
    monkeypatch.setattr(search_service, "bm25_search", lambda **kwargs: [])


def test_prompt_survives_when_reranking_rejects_everything(
    monkeypatch, retrieval_stubs
):
    """The failure this fixes: a relevant document, scored below the floor."""

    monkeypatch.setattr(search_service, "rerank_documents", lambda **kwargs: [])

    result = search_service.search_documents(
        "What quarterly revenue was reported?",
        user_id=7,
        conversation_id=3,
    )

    assert result["prompt"] is not None
    assert ANSWER in result["prompt"]
    assert result["documents"] == [ANSWER]


def test_reranked_order_is_kept_when_reranking_returns_documents(
    monkeypatch, retrieval_stubs
):
    """The fallback must not interfere when reranking works normally."""

    monkeypatch.setattr(search_service, "rerank_documents", lambda **kwargs: [ANSWER])

    result = search_service.search_documents(
        "What quarterly revenue was reported?",
        user_id=7,
        conversation_id=3,
    )

    assert result["prompt"] is not None
    assert result["documents"] == [ANSWER]
