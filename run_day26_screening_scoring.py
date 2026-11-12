import json
from pathlib import Path

from src.screening_scoring import score_screening


ROOT = Path(__file__).resolve().parent

DATA_FILE = (
    ROOT
    / "data"
    / "day26_screening_scoring"
    / "sample_screening_data.json"
)

OUTPUT_DIR = ROOT / "outputs" / "day26"


def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    dataset = json.loads(
        DATA_FILE.read_text(encoding="utf-8-sig")
    )

    results = []

    print()
    print("=" * 72)
    print("DAY 26 - SCREENING SCORING ENGINE")
    print("=" * 72)

    for candidate in dataset:

        result = score_screening(
            candidate_id=candidate["candidate_id"],
            questions=candidate["questions"],
        )

        results.append(result)

        print()
        print("-" * 72)
        print(f"Candidate ID: {result['candidate_id']}")
        print(f"Questions Scored: {result['question_count']}")
        print(f"Overall Screening Score: {result['overall_screening_score']}/100")
        print(f"Classification: {result['classification']}")

        print()
        print("Parameter Averages:")

        for name, score in result["parameter_averages"].items():
            print(f"  {name.title()}: {score}/100")

        print()
        print("Per-question Breakdown:")

        for question in result["question_scores"]:
            print(
                f"  {question['question_id']}: "
                f"{question['weighted_score']}/100"
            )

    results_path = (
        OUTPUT_DIR
        / "day26_screening_scores.json"
    )

    results_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = {
        "day": 26,
        "title": "Screening Scoring Engine",
        "status": "COMPLETED",
        "candidate_count": len(results),
        "total_questions_scored": sum(
            result["question_count"] for result in results
        ),
        "scoring_parameters": {
            "clarity": 0.25,
            "relevance": 0.35,
            "completeness": 0.25,
            "consistency": 0.15,
        },
        "score_scale": "0-100",
        "aggregation": (
            "Arithmetic mean of per-question weighted scores."
        ),
        "generated_files": [
            "outputs/day26/day26_screening_scores.json",
            "outputs/day26/day26_screening_scoring_report.json",
        ],
    }

    report_path = (
        OUTPUT_DIR
        / "day26_screening_scoring_report.json"
    )

    report_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print()
    print("=" * 72)
    print("DAY 26 DEMO COMPLETED")
    print("=" * 72)
    print(f"Candidates processed: {len(results)}")
    print(
        "Total questions scored: "
        f"{report['total_questions_scored']}"
    )
    print("Scoring parameters: IMPLEMENTED")
    print("Per-question scoring: IMPLEMENTED")
    print("Score normalization: IMPLEMENTED")
    print("Aggregate screening score: IMPLEMENTED")
    print("Explainable scoring output: IMPLEMENTED")
    print()
    print("Generated files:")
    print(f"  {results_path.relative_to(ROOT)}")
    print(f"  {report_path.relative_to(ROOT)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
