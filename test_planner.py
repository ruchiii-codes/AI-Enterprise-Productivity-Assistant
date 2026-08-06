from server.services.planner_service import plan_route


queries = [
    "Hi",
    "Hello",
    "Summarize this PDF",
    "Give me summary",
    "What is Hybrid Search?",
    "Explain BM25",
    "How many PDFs have I uploaded?",
]

for query in queries:

    route = plan_route(query)

    print(f"{query} ---> {route.value}")