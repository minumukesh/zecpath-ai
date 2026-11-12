import json
from pathlib import Path

from src.screening_report import generate_sample_reports


INPUT_PATH = Path("data/day28_screening_reports/sample_candidates.json")
OUTPUT_DIRECTORY = Path("outputs/day28")


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Sample input file not found: {INPUT_PATH}")

    raw_text = INPUT_PATH.read_text(encoding="utf-8-sig")
    data = json.loads(raw_text)

    candidates = data.get("candidates", [])

    if not candidates:
        raise ValueError("No sample candidates found in the input file.")

    result = generate_sample_reports(
        candidates,
        output_directory=OUTPUT_DIRECTORY,
    )

    print("=" * 65)
    print("DAY 28 - AI SCREENING REPORT GENERATOR")
    print("=" * 65)
    print(f"Sample candidates processed: {result['summary']['total_candidates']}")
    print(f"Reports generated: {result['summary']['reports_generated']}")
    print()

    for item in result["results"]:
        candidate = item["report"]["candidate"]
        summary = item["report"]["screening_summary"]

        print(f"Candidate ID: {candidate['candidate_id']}")
        print(f"Candidate: {candidate['candidate_name']}")
        print(f"Role: {candidate['job_role']}")
        print(f"ATS score: {summary['ats_score']}")
        print(f"Missing data fields: {len(summary['missing_data'])}")
        print(f"JSON report: {item['json_path']}")
        print(f"Markdown report: {item['markdown_path']}")
        print("-" * 65)

    print(f"Summary report: {result['summary_path']}")
    print()
    print("DAY 28 DEMO COMPLETED")
    print("=" * 65)


if __name__ == "__main__":
    main()
