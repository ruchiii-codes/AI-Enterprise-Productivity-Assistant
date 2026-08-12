from unittest.mock import patch

from server.services.query_rewrite_service import rewrite_query


def test_rewrite_query():
    with patch(
        "server.services.query_rewrite_service.generate_response",
        return_value="Python exception handling best practices",
    ):
        result = rewrite_query(
            "Can you tell me what are the best practices for handling exceptions in Python?"
        )

    assert result == "Python exception handling best practices"