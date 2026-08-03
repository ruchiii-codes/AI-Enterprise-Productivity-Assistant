import json

from server.services.planner_service import plan_route


def evaluate_agents():

    with open(
        "data/agent_evaluation_questions.json",
        "r",
        encoding="utf-8",
    ) as f:

        questions = json.load(f)

    total = len(questions)
    correct = 0
    results = []

    for item in questions:

        predicted = plan_route(item["question"]).value
        expected = item["expected_route"]

        is_correct = predicted == expected

        if is_correct:
            correct += 1

        results.append(
            {
                "question": item["question"],
                "expected": expected,
                "predicted": predicted,
                "correct": is_correct,
            }
        )

    accuracy = (correct / total) * 100

    return {
        "accuracy": round(accuracy, 2),
        "correct": correct,
        "total": total,
        "results": results,
    }