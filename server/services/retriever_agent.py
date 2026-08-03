from server.services.search_service import search_documents


def retrieve(query: str):
    """
    Retriever Agent

    Responsible for retrieving
    relevant documents for the planner.
    """

    return search_documents(query)