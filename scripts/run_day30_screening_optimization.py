import json
from pathlib import Path

from src.screening_optimization import run_evaluation


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "day30" / "screening_test_cases.json"
OUTPUT_DIR = ROOT / "outputs" / "day30"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with DATA_FILE.open("r", encoding="utf-8-sig") as file:
        cases = json.load(file)

    report = run_evaluation(cases)

    json_path = OUTPUT_DIR / "day30_screening_test_report.json"
    markdown_path = OUTPUT_DIR / "day30_screening_test_report.md"

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    baseline = report["baseline_metrics"]
    optimized = report["optimized_metrics"]
    optimization = report["optimization"]

    lines = [
        "# Day 30: Screening System Testing & Optimization",
        "",
        "## Objective",
        "",
        "Test simulated screening responses, compare decisions with predefined",
        "human evaluation labels, review intent detection, and tune scoring thresholds.",
        "",
        "## Workflow",
        "",
        "Simulated Candidate Responses",
        "→ Intent Detection",
        "→ Response Scoring",
        "→ AI Decision",
        "→ Comparison with Human Evaluation",
        "→ Threshold Optimization",
        "→ Optimized Evaluation Report",
        "",
        "## Dataset",
        "",
        f"- Simulated cases: {len(cases)}",
        "- Expected decisions are predefined sample labels.",
        "",
        "## Baseline Results",
        "",
        f"- Accept threshold: {report['baseline_thresholds']['accept']}",
        f"- Review threshold: {report['baseline_thresholds']['review']}",
        f"- Decision accuracy: {baseline['decision_accuracy']:.2%}",
        f"- Intent accuracy: {baseline['intent_accuracy']:.2%}",
        f"- False rejections: {baseline['false_rejections']}",
        f"- False acceptances: {baseline['false_acceptances']}",
        "",
        "## Selected Thresholds",
        "",
        f"- Accept threshold: {optimization['selected_accept_threshold']}",
        f"- Review threshold: {optimization['selected_review_threshold']}",
        "",
        "## Optimized Results",
        "",
        f"- Decision accuracy: {optimized['decision_accuracy']:.2%}",
        f"- Intent accuracy: {optimized['intent_accuracy']:.2%}",
        f"- False rejections: {optimized['false_rejections']}",
        f"- False acceptances: {optimized['false_acceptances']}",
        "",
        "## Candidate Evaluation",
        "",
        "| Candidate | Expected Intent | Detected Intent | Score | Human Label | AI Decision |",
        "|---|---|---|---:|---|---|",
    ]

    for result in report["results"]:
        lines.append(
            f"| {result['candidate_id']} "
            f"| {result['expected_intent']} "
            f"| {result['detected_intent']} "
            f"| {result['score_breakdown']['total_score']:.2f} "
            f"| {result['human_decision']} "
            f"| {result['ai_decision']} |"
        )

    lines.extend([
        "",
        "## Score Breakdown",
        "",
        "Each answer receives an explainable score:",
        "",
        "- Clarity: 25%",
        "- Relevance: 35%",
        "- Completeness: 25%",
        "- Consistency: 15%",
        "",
        "## Limitations",
        "",
        "- The test dataset uses simulated candidate responses.",
        "- Human decisions are predefined labels, not live recruiter judgments.",
        "- Intent detection and scoring are rule-based prototypes.",
        "- Threshold tuning on a small dataset does not prove general performance.",
        "- Borderline and uncertain responses should receive human review.",
        "",
        "## Deliverables",
        "",
        "- Screening system test report",
        "- Baseline and optimized metric comparison",
        "- Threshold tuning results",
        "- Candidate-level decision explanations",
        "",
        "## Conclusion",
        "",
        "The implementation evaluates sample screening responses, compares",
        "AI decisions with expected labels, and searches for a threshold that",
        "reduces weighted evaluation errors. The results are a prototype and",
        "must be validated on a larger independent dataset before production use.",
        "",
    ])

    markdown_path.write_text("\n".join(lines), encoding="utf-8")

    print("=" * 68)
    print("DAY 30 - SCREENING SYSTEM TESTING & OPTIMIZATION")
    print("=" * 68)
    print(f"Simulated responses processed: {len(cases)}")
    print("Simulated screening evaluation: COMPLETED")
    print("Intent detection: IMPLEMENTED")
    print("Human-label comparison: IMPLEMENTED")
    print("Explainable response scoring: IMPLEMENTED")
    print("Threshold optimization: IMPLEMENTED")
    print("False-rejection tracking: IMPLEMENTED")
    print("-" * 68)
    print("BASELINE")
    print(f"  Decision accuracy: {baseline['decision_accuracy']:.2%}")
    print(f"  Intent accuracy: {baseline['intent_accuracy']:.2%}")
    print(f"  False rejections: {baseline['false_rejections']}")
    print(f"  False acceptances: {baseline['false_acceptances']}")
    print("-" * 68)
    print("OPTIMIZED EVALUATION")
    print(f"  Accept threshold: {optimization['selected_accept_threshold']}")
    print(f"  Review threshold: {optimization['selected_review_threshold']}")
    print(f"  Decision accuracy: {optimized['decision_accuracy']:.2%}")
    print(f"  Intent accuracy: {optimized['intent_accuracy']:.2%}")
    print(f"  False rejections: {optimized['false_rejections']}")
    print(f"  False acceptances: {optimized['false_acceptances']}")
    print("-" * 68)
    print(f"JSON report: {json_path.relative_to(ROOT)}")
    print(f"Markdown report: {markdown_path.relative_to(ROOT)}")
    print("DAY 30 DEMO COMPLETED")
    print("=" * 68)


if __name__ == "__main__":
    main()
