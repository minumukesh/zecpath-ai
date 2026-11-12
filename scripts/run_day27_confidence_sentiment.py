import json
from pathlib import Path

from src.confidence_sentiment import analyze_screening


ROOT = Path(__file__).resolve().parent

DATA_FILE = (
    ROOT
    / "data"
    / "day27_confidence_sentiment"
    / "sample_responses.json"
)

OUTPUT_DIR = ROOT / "outputs" / "day27"


def main():
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    dataset = json.loads(
        DATA_FILE.read_text(
            encoding="utf-8-sig"
        )
    )

    results = []

    print()
    print("=" * 72)
    print("DAY 27 - CONFIDENCE & SENTIMENT SIGNAL ANALYSIS")
    print("=" * 72)

    for candidate in dataset:
        result = analyze_screening(
            candidate_id=candidate["candidate_id"],
            responses=candidate["responses"],
        )

        results.append(result)

        print()
        print("-" * 72)
        print(f"Candidate: {result['candidate_id']}")
        print(f"Responses analyzed: {result['response_count']}")

        for response in result["responses"]:
            print()
            print(f"Response ID: {response['response_id']}")
            print(
                "Words:",
                response["response_metrics"]["word_count"]
            )
            print(
                "Pace:",
                response["response_metrics"]["pace_label"]
            )
            print(
                "Words per minute:",
                response["response_metrics"]["words_per_minute"]
            )
            print(
                "Hesitation count:",
                response["confidence_analysis"]["hesitation_count"]
            )
            print(
                "Uncertainty count:",
                response["confidence_analysis"]["uncertainty_count"]
            )
            print(
                "Sentiment:",
                response["sentiment_analysis"]["sentiment"]
            )
            print(
                "Sentiment score:",
                response["sentiment_analysis"]["sentiment_score"]
            )

        print()
        print("Behavioral Indicators Report:")
        print(
            json.dumps(
                result["behavioral_indicators_report"],
                indent=2
            )
        )

        print(
            "Potential contradictions:",
            result["contradiction_analysis"][
                "potential_contradiction_count"
            ]
        )

    results_path = (
        OUTPUT_DIR / "day27_analysis_results.json"
    )

    results_path.write_text(
        json.dumps(
            results,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    summary = {
        "day": 27,
        "title": "Confidence & Sentiment Signal Analysis",
        "status": "COMPLETED",
        "candidates_processed": len(results),
        "responses_analyzed": sum(
            item["response_count"]
            for item in results
        ),
        "features": [
            "Hesitation detection",
            "Response length measurement",
            "Speaking pace when duration is provided",
            "Positive/negative/neutral sentiment",
            "Uncertainty detection",
            "Potential contradiction detection",
            "Communication strength indicators",
            "Behavioral indicators report",
        ],
        "generated_files": [
            "outputs/day27/day27_analysis_results.json",
            "outputs/day27/day27_behavioral_report.json",
        ],
    }

    report_path = (
        OUTPUT_DIR / "day27_behavioral_report.json"
    )

    report_path.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8"
    )

    print()
    print("=" * 72)
    print("DAY 27 DEMO COMPLETED")
    print("=" * 72)
    print(f"Candidates processed: {len(results)}")
    print(
        "Responses analyzed:",
        summary["responses_analyzed"]
    )
    print("Hesitation detection: IMPLEMENTED")
    print("Response length and pace: IMPLEMENTED")
    print("Sentiment analysis: IMPLEMENTED")
    print("Uncertainty detection: IMPLEMENTED")
    print("Potential contradiction detection: IMPLEMENTED")
    print("Communication strength indicators: IMPLEMENTED")
    print("Behavioral indicators report: GENERATED")
    print()
    print("Generated files:")
    print("  outputs/day27/day27_analysis_results.json")
    print("  outputs/day27/day27_behavioral_report.json")
    print("=" * 72)


if __name__ == "__main__":
    main()
