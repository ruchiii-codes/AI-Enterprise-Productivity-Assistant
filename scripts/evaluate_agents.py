import json

from server.config import settings
from server.services.evaluation.agent_evaluation_service import evaluate_agents


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


    report_path = settings.DATA_DIR / "agent_evaluation_report.json"

    with open(
        report_path,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            report,
            f,
            indent=4,
        )

    print(f"Report saved to {report_path}")


if __name__ == "__main__":
    main()
