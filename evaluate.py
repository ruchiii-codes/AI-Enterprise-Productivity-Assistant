import json

from server.services.evaluation_service import evaluate_retriever


def main():

    report = evaluate_retriever()

    print("\n========== Evaluation Report ==========")

    print(f"Questions Evaluated : {report['total_questions']}")
    print(f"Hit Rate            : {report['hit_rate']:.2%}")
    print(f"Precision           : {report['precision']:.2%}")
    print(f"Recall              : {report['recall']:.2%}")
    print(f"MRR                 : {report['mrr']:.2%}")

    print("=======================================\n")

    with open(
        "data/evaluation_report.json",
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
        )


if __name__ == "__main__":
    main()