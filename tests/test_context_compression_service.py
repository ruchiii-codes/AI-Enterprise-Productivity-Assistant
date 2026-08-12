from unittest.mock import patch

from server.services.context_compression_service import compress_context


def test_compress_context():
    mock_response = (
        "JWT authentication uses signed tokens. "
        "The server validates the token before granting access."
    )

    documents = [
        "JWT authentication uses signed tokens. "
        "The server validates the token before granting access. "
        "This document also discusses unrelated database indexing."
    ]

    with patch(
        "server.services.context_compression_service.generate_response",
        return_value=mock_response,
    ):
        result = compress_context(
            "How does JWT authentication work?",
            documents,
        )

    assert result == mock_response