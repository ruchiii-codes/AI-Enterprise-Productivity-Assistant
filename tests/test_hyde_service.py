from unittest.mock import patch

from server.services.hyde_service import generate_hypothetical_document


def test_generate_hypothetical_document():
    mock_response = (
        "JWT authentication uses signed tokens containing claims. "
        "The server validates the token before granting access."
    )

    with patch(
        "server.services.hyde_service.generate_response",
        return_value=mock_response,
    ):
        result = generate_hypothetical_document(
            "How does JWT authentication work?"
        )

    assert result == mock_response