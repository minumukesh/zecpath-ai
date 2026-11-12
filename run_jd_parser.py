from pathlib import Path
import json

from src.jd_parser.parser import (
    parse_job_description,
    save_parsed_jd
)


BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = (
    BASE_DIR
    / "data"
    / "job_descriptions"
    / "raw"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "job_descriptions"
    / "parsed"
)

LOG_DIR = (
    BASE_DIR
    / "outputs"
    / "jd_logs"
)


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    results = []

    print("=" * 60)
    print("ZECPATH - JOB DESCRIPTION PARSER")
    print("=" * 60)

    for file_path in sorted(INPUT_DIR.glob("*.txt")):

        print(
            f"Processing: {file_path.name}"
        )

        try:

            result = parse_job_description(
                str(file_path)
            )

            output = save_parsed_jd(
                result,
                str(OUTPUT_DIR)
            )

            results.append({
                "file": file_path.name,
                "status": "PASS",
                "output": output
            })

            print("  PASS")

        except Exception as error:

            results.append({
                "file": file_path.name,
                "status": "FAIL",
                "error": str(error)
            })

            print(
                f"  FAIL: {error}"
            )

    log_file = (
        LOG_DIR
        / "jd_parsing_log.json"
    )

    with open(
        log_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )

    passed = sum(
        1
        for item in results
        if item["status"] == "PASS"
    )

    failed = sum(
        1
        for item in results
        if item["status"] == "FAIL"
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
