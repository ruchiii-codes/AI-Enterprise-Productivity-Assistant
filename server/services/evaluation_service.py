import json
from server.services.search_service import search_documents

def load_evaluation_questions():

    with open(
        "data/evaluation_questions.json",
        "r",
        encoding="utf-8"
    ) as file:

        questions = json.load(file)

    return questions


def calculate_hit_rate(
    retrieved_chunks: list[str],
    expected_keywords: list[str],
) -> int:

    for chunk in retrieved_chunks:

        chunk = chunk.lower()

        for keyword in expected_keywords:

            if keyword.lower() in chunk:
                return 1

    return 0


def calculate_precision(
    retrieved_chunks: list[str],
    expected_keywords: list[str],
) -> float:

    if not retrieved_chunks:
        return 0.0

    relevant = 0

    for chunk in retrieved_chunks:

        chunk = chunk.lower()

        for keyword in expected_keywords:

            if keyword.lower() in chunk:
                relevant += 1
                break

    return relevant / len(retrieved_chunks)


def calculate_recall(
    retrieved_chunks: list[str],
    expected_keywords: list[str],
) -> float:

    if not expected_keywords:
        return 0.0

    found_keywords = set()

    for chunk in retrieved_chunks:

        chunk = chunk.lower()

        for keyword in expected_keywords:

            if keyword.lower() in chunk:
                found_keywords.add(keyword.lower())

    return len(found_keywords) / len(expected_keywords)


def calculate_mrr(
    retrieved_chunks: list[str],
    expected_keywords: list[str],
) -> float:

    for index, chunk in enumerate(retrieved_chunks, start=1):

        chunk = chunk.lower()

        for keyword in expected_keywords:

            if keyword.lower() in chunk:
                return 1 / index

    return 0.0


def evaluate_retriever():

    questions = load_evaluation_questions()

    total_hit_rate = 0
    total_precision = 0
    total_recall = 0
    total_mrr = 0

    total_questions = len(questions)

    if total_questions == 0:
        return {
            "total_questions": 0,
            "hit_rate": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "mrr": 0.0,
        }

    for item in questions:

        question = item["question"]
        expected_keywords = item["expected_keywords"]

        # Replace this with your actual retrieval function
        results = search_documents(question)
        retrieved_chunks = results["documents"]

        hit = calculate_hit_rate(
            retrieved_chunks,
            expected_keywords,
        )

        precision = calculate_precision(
            retrieved_chunks,
            expected_keywords,
        )

        recall = calculate_recall(
            retrieved_chunks,
            expected_keywords,
        )

        mrr = calculate_mrr(
            retrieved_chunks,
            expected_keywords,
        )

        total_hit_rate += hit
        total_precision += precision
        total_recall += recall
        total_mrr += mrr

    report = {
        "total_questions": total_questions,
        "hit_rate": total_hit_rate / total_questions,
        "precision": total_precision / total_questions,
        "recall": total_recall / total_questions,
        "mrr": total_mrr / total_questions,
    }

    return report