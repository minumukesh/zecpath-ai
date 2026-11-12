import json
from pathlib import Path

from src.edge_case_handling import run_edge_case_evaluation


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "day31" / "edge_case_test_cases.json"
OUTPUT_DIR = ROOT / "outputs" / "day31"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with DATA_FILE.open("r", encoding="utf-8-sig") as file:
        cases = json.load(file)

    report = run_edge_case_evaluation(cases)

    json_path = OUTPUT_DIR / "day31_edge_case_report.json"
    markdown_path = OUTPUT_DIR / "day31_edge_case_report.md"

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    lines = [
        "# Day 31: Edge Case & Failure Handling",
        "",
        "## Objective",
        "",
        "Check whether the screening flow handles difficult inputs safely.",
        "",
        "## Workflow",
        "",
        "Candidate Transcript",
        "→ Check Audio Quality",
        "→ Check Language Mixing",
        "→ Check Missing Answers",
        "→ Check Background Noise",
        "→ Apply Safety Checks",
        "→ Continue, Clarify, or Send for Human Review",
        "",
        "## Test Summary",
        "",
        f"- Total simulated cases: {report['total_cases']}",
        "",
        "### Actions",
        "",
    ]

    for action, count in sorted(report["action_counts"].items()):
        lines.append(f"- {action}: {count}")

    lines.extend([
        "",
        "## Individual Test Results",
        "",
        "| Case | Scenario | Audio | Language | Answer | Noise | Safety | Action |",
        "|---|---|---|---|---|---|---|---|",
    ])

    for result in report["results"]:
        lines.append(
            f"| {result['case_id']} "
            f"| {result['scenario']} "
            f"| {result['audio_quality']['status']} "
            f"| {result['language_mixing']['status']} "
            f"| {result['missing_answer']['status']} "
            f"| {'YES' if result['background_noise']['noise_detected'] else 'NO'} "
            f"| {'FLAGGED' if result['safety_check']['safety_flag'] else 'CLEAR'} "
            f"| {result['decision']['action']} |"
        )

    lines.extend([
        "",
        "## Failure Handling",
        "",
        "- Poor audio: request a repeat or clarification.",
        "- Mixed or uncertain language: request clarification.",
        "- Missing answer: ask the candidate to respond again.",
        "- Background noise: request a clearer response.",
        "- Repeated failure: send the response for human review.",
        "- Unsafe request: use a safe fallback.",
        "",
        "## Important Limitations",
        "",
        "- The dataset uses simulated transcript text.",
        "- This implementation does not transcribe real audio.",
        "- Language detection is based on a small phrase dictionary.",
        "- Audio quality uses provided metadata and text markers.",
        "- Human review is used instead of automatic rejection when unresolved.",
        "",
        "## Deliverables",
        "",
        "- Edge-case handling engine",
        "- Retry and clarification logic",
        "- Safety fallback",
        "- JSON and Markdown test reports",
        "",
    ])

    markdown_path.write_text("\n".join(lines), encoding="utf-8")

    print("=" * 68)
    print("DAY 31 - EDGE CASE & FAILURE HANDLING")
    print("=" * 68)
    print(f"Simulated cases processed: {report['total_cases']}")
    print("Poor audio handling: IMPLEMENTED")
    print("Language-mixing checks: IMPLEMENTED")
    print("Missing-answer handling: IMPLEMENTED")
    print("Background-noise checks: IMPLEMENTED")
    print("Retry and clarification logic: IMPLEMENTED")
    print("Safety fallback: IMPLEMENTED")
    print("Human-review fallback: IMPLEMENTED")
    print("-" * 68)
    print("ACTION SUMMARY")

    for action, count in sorted(report["action_counts"].items()):
        print(f"{action}: {count}")

    print("-" * 68)
    print(f"JSON report: {json_path.relative_to(ROOT)}")
    print(f"Markdown report: {markdown_path.relative_to(ROOT)}")
    print("DAY 31 DEMO COMPLETED")
    print("=" * 68)


if __name__ == "__main__":
    main()
