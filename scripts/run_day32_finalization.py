from pathlib import Path

from src.day32_finalization import (
    load_demo_cases,
    build_finalization_report,
    write_reports,
)


ROOT = Path(__file__).resolve().parent


def main():
    dataset_path = ROOT / "data" / "day32" / "finalization_demo_cases.json"

    cases = load_demo_cases(dataset_path)
    report = build_finalization_report(ROOT, cases)
    generated = write_reports(ROOT, report)

    print("=" * 68)
    print("DAY 32 - SCREENING SYSTEM FINALIZATION")
    print("=" * 68)

    print("\nPROJECT COMPONENT INSPECTION")
    inspection = report["project_inspection"]
    print(f"Components checked: {inspection['components_checked']}")
    print(f"Components found: {inspection['components_found']}")
    print(f"Components missing: {inspection['components_missing']}")

    for name, component in inspection["components"].items():
        status = "FOUND" if component["exists"] else "NOT FOUND"
        print(f"{name}: {status}")

    print("\nFINALIZATION DEMO")
    print(f"Demo cases processed: {report['demo']['cases_processed']}")

    for result in report["demo"]["results"]:
        print("-" * 50)
        print(f"Candidate: {result['candidate_id']}")
        print(f"Role: {result['role']}")
        print(f"Demo keyword-overlap score: {result['demo_keyword_overlap_score']}")
        print(f"Demo result: {result['demo_result']}")
        print("Note: This is not the official ATS score.")

    print("\nGENERATED DOCUMENTS")
    for label, path in generated.items():
        print(f"{label}: {path.relative_to(ROOT)}")

    print("\nDAY 32 DEMO AND DOCUMENT GENERATION COMPLETED")
    print("=" * 68)


if __name__ == "__main__":
    main()
