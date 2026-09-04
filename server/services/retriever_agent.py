from server.services.search_service import search_documents


def retrieve(
    query: str,
    history=None,
    user_id: int | None = None,
    conversation_id: int | None = None,
):
    """
    Retriever Agent

    Responsible for retrieving
    relevant documents for the planner.
    """

    return search_documents(
        query,
        history=history,
        user_id=user_id,
        conversation_id=conversation_id,
    )