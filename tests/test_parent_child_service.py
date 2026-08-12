from server.services.parent_child_service import create_parent_child_chunks


def test_create_parent_child_chunks():
    text = " ".join(
        f"This is sentence number {i} about enterprise AI systems."
        for i in range(300)
    )

    results = create_parent_child_chunks(text)

    assert len(results) > 0

    first = results[0]

    assert "parent_id" in first
    assert "child_id" in first
    assert "parent" in first
    assert "child" in first

    assert len(first["parent"]) >= len(first["child"])