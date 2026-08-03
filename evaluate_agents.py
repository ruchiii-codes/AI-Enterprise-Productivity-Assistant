import json

from server.services.agent_evaluation_service import evaluate_agents


def main():

    report = evaluate_agents()

    print("\n===== Agent Evaluation Report =====\n")

    print(f"Accuracy : {report['accuracy']}%")
    print(f"Correct  : {report['correct']}")
    print(f"Total    : {report['total']}\n")

    for result in report["results"]:

        status = "PASS" if result["correct"] else "FAIL"

        print(f"[{status}] {result['question']}")
        print(f"Expected : {result['expected']}")
        print(f"Predicted: {result['predicted']}")
        print()


    with open(
        "data/agent_evaluation_report.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            report,
            f,
            indent=4,
        )

    print("Report saved to data/agent_evaluation_report.json")


if __name__ == "__main__":
    main()