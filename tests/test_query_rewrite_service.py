from unittest.mock import patch

from server.services.query_rewrite_service import (
    query_rewrite_cache,
    rewrite_query,
)


def test_rewrite_query():
    query_rewrite_cache.clear()

    with patch(
        "server.services.query_rewrite_service.generate_response",
        return_value="AI enterprise assistant architecture",
    ) as mock_generate:

        result = rewrite_query(
            "Can you tell me about the architecture of the AI enterprise assistant?"
        )

        assert result == "AI enterprise assistant architecture"
        mock_generate.assert_called_once()


def test_rewrite_query_uses_cache():
    query_rewrite_cache.clear()

    with patch(
        "server.services.query_rewrite_service.generate_response",
        return_value="AI enterprise assistant architecture",
    ) as mock_generate:

        question = "Tell me about the AI enterprise assistant architecture."

        first_result = rewrite_query(question)
        second_result = rewrite_query(question)

        assert first_result == second_result
        mock_generate.assert_called_once()