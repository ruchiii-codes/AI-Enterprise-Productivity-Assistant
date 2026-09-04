from rank_bm25 import BM25Okapi

bm25_index: BM25Okapi | None = None
document_chunks: list[str] = []

# Metadata corresponding to each chunk in document_chunks
document_metadata: list[dict] = []