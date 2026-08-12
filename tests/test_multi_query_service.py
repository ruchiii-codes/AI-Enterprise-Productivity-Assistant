from unittest.mock import patch

from server.services.multi_query_service import generate_multi_queries


def test_generate_multi_queries():
    mock_response = """Python authentication best practices
Handling authentication errors in Python
Python login and token error handling"""

    with patch(
        "server.services.multi_query_service.generate_response",
        return_value=mock_response,
    ):
        queries = generate_multi_queries(
            "How do I handle authentication errors in Python?"
        )

    assert len(queries) == 3
    assert queries[0] == "Python authentication best practices"
    assert queries[1] == "Handling authentication errors in Python"
    assert queries[2] == "Python login and token error handling"