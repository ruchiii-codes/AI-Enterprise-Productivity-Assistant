from server.services.chroma_service import get_parent_documents


def test_get_parent_documents():
    results = {
        "documents": [[
            "child 1",
            "child 2",
            "child 3",
        ]],
        "metadatas": [[
            {
                "parent_id": 1,
                "parent": "parent 1",
            },
            {
                "parent_id": 1,
                "parent": "parent 1",
            },
            {
                "parent_id": 2,
                "parent": "parent 2",
            },
        ]],
    }

    result = get_parent_documents(results)

    assert result["documents"][0] == [
        "parent 1",
        "parent 2",
    ]