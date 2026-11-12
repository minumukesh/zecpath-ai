import json
from pathlib import Path

from src.resume_extraction.extractor import process_resume_folder


BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "data" / "resumes" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "resumes" / "extracted"
LOG_DIR = BASE_DIR / "outputs" / "test_logs"


def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("ZECPATH - RESUME TEXT EXTRACTION ENGINE")
    print("=" * 60)

    print(f"Input : {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print()

    results = process_resume_folder(
        str(INPUT_DIR),
        str(OUTPUT_DIR)
    )

    passed = sum(
        1 for item in results
        if item["status"] == "PASS"
    )

    failed = sum(
        1 for item in results
        if item["status"] == "FAIL"
    )

    log = {
        "project": "ZECPATH",
        "task": "Day 5 - Resume Text Extraction Engine",
        "total_files": len(results),
        "passed": passed,
        "failed": failed,
        "results": results
    }

    log_file = LOG_DIR / "extraction_test_log.json"

    with open(
        log_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            log,
            file,
            indent=4,
            ensure_ascii=False
        )

    for item in results:
        print(
            f"{item['file_name']}: "
            f"{item['status']}"
        )

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total : {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Log   : {log_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
