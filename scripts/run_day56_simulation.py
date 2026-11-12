import json
from pathlib import Path

from src.day56_simulation.engine import (
    HiringPipeline,
    save_report
)


def main():

    dataset_path = Path(
        "data/day56/simulation_dataset.json"
    )

    with dataset_path.open(
        "r",
        encoding="utf-8-sig"
    ) as file:

        dataset = json.load(file)

    pipeline = HiringPipeline()

    print("\n================================================")
    print(" DAY 56 - FULL SYSTEM SIMULATION")
    print("================================================")

    print("\nPipeline stages:")

    for index, stage in enumerate(
        pipeline.stage_names,
        start=1
    ):

        print(f"{index}. {stage.replace('_', ' ').title()}")

    report = pipeline.run_simulation(
        dataset["candidates"]
    )

    print("\n================================================")
    print(" CANDIDATE RESULTS")
    print("================================================")

    for result in report["results"]:

        print("\nCandidate:", result["candidate_name"])
        print("Role:", result["role"])

        for stage, details in result["stages"].items():

            print(
                f"{stage.upper()}: "
                f"{details['score']} "
                f"({details['status']})"
            )

        print(
            "AI decision:",
            result["ai_decision"]["recommendation"]
        )

        print(
            "Human decision:",
            result["human_comparison"]["human_decision"]
        )

        print(
            "AI-human comparison:",
            result["human_comparison"]["comparison"]
        )

        print(
            "Inconsistencies:",
            len(result["inconsistencies"])
        )

    print("\n================================================")
    print(" HUMAN VS AI ANALYSIS")
    print("================================================")

    comparison = report["human_ai_comparison"]

    print("Agreements:", comparison["agreements"])
    print("Disagreements:", comparison["disagreements"])
    print(
        "Agreement rate:",
        f"{comparison['agreement_rate']:.2%}"
    )

    print("\n================================================")
    print(" SYSTEM PERFORMANCE")
    print("================================================")

    performance = report["performance_analysis"]

    print("Candidates:", performance["candidate_count"])

    print(
        "Average processing time:",
        performance["average_processing_time_seconds"]
    )

    print(
        "Maximum processing time:",
        performance["maximum_processing_time_seconds"]
    )

    print("\nAverage stage scores:")

    for stage, score in performance["average_stage_scores"].items():

        print(f"{stage}: {score}")

    print("\nTotal inconsistencies:", report["total_inconsistencies"])

    print("\n================================================")
    print(" IMPROVEMENT RECOMMENDATIONS")
    print("================================================")

    for recommendation in report["improvement_recommendations"]:

        print("-", recommendation)

    output_files = save_report(report)

    print("\n================================================")
    print(" DAY 56 REPORTS GENERATED")
    print("================================================")

    for name, path in output_files.items():

        print(name, ":", path)


if __name__ == "__main__":
    main()
