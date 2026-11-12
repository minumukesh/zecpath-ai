import json
from pathlib import Path

from src.hr_interview_optimization.engine import (
    clean_transcript,
    handle_follow_up,
    calculate_refined_score,
    evaluate_decisions,
    optimize_threshold,
    benchmark_processing
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs/day42"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    cases = json.loads(
        (ROOT / "data/day42/optimization_cases.json").read_text(encoding="utf-8-sig")
    )

    baseline = evaluate_decisions(cases, 70)

    optimization = optimize_threshold(cases)

    selected = optimization["selected_threshold"]

    optimized = evaluate_decisions(cases, selected)

    transcripts = [
        {
            "candidate_id": case["candidate_id"],
            **clean_transcript(case["transcript"])
        }
        for case in cases
    ]

    refined = calculate_refined_score({
        "answer_relevance": 85,
        "communication": 80,
        "confidence": 75,
        "consistency": 90
    })

    followups = [
        handle_follow_up(""),
        handle_follow_up("Yes"),
        handle_follow_up("I developed a Python project."),
        handle_follow_up(
            "I developed a Python project.",
            previous_answer="I developed a Python project."
        )
    ]

    benchmark = benchmark_processing(cases, selected)

    report = {
        "day": 42,
        "module": "Optimization and Stability",
        "baseline": baseline,
        "threshold_optimization": optimization,
        "optimized": optimized,
        "transcript_cleanup": transcripts,
        "refined_scoring": refined,
        "follow_up_examples": followups,
        "processing_benchmark": benchmark,
        "limitations": [
            "Demonstration dataset is small.",
            "Thresholds require validation on representative data.",
            "Processing time depends on the machine.",
            "Human review remains necessary."
        ]
    }

    (OUT / "day42_optimization_report.json").write_text(
        json.dumps(report, indent=4), encoding="utf-8-sig"
    )

    markdown = (
        "# Day 42 - Optimization and Stability\n\n"
        "## Baseline Evaluation\n"
        f"- Accuracy: {baseline['accuracy']}%\n"
        f"- False positives: {baseline['false_positive']}\n"
        f"- False negatives: {baseline['false_negative']}\n\n"
        "## Optimized Evaluation\n"
        f"- Selected threshold: {selected}\n"
        f"- Accuracy: {optimized['accuracy']}%\n"
        f"- False positives: {optimized['false_positive']}\n"
        f"- False negatives: {optimized['false_negative']}\n\n"
        "## Other Improvements\n"
        "- Follow-up stability checks\n"
        "- Score validation and refined weighted scoring\n"
        "- Transcript cleanup\n"
        "- Processing benchmark\n\n"
        "Results are based on the included demonstration dataset."
    )

    (OUT / "day42_optimization_report.md").write_text(
        markdown, encoding="utf-8-sig"
    )

    print("=" * 60)
    print("DAY 42 - OPTIMIZATION AND STABILITY")
    print("=" * 60)
    print("Cases:", len(cases))
    print("Baseline accuracy:", baseline["accuracy"], "%")
    print("Baseline false positives:", baseline["false_positive"])
    print("Baseline false negatives:", baseline["false_negative"])
    print("Selected threshold:", selected)
    print("Optimized accuracy:", optimized["accuracy"], "%")
    print("Optimized false positives:", optimized["false_positive"])
    print("Optimized false negatives:", optimized["false_negative"])
    print("Transcript cleanup: COMPLETED")
    print("Follow-up stability: COMPLETED")
    print("Scoring refinement: COMPLETED")
    print("Processing benchmark:", benchmark)
    print("JSON and Markdown reports generated.")
    print("DAY 42 DEMO COMPLETED")

if __name__ == "__main__":
    main()
