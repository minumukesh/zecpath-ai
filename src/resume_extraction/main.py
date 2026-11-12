from pathlib import Path

from .extractor import process_resume_folder


# Find the main ZECPATH-AI project folder
BASE_DIR = Path(__file__).resolve().parents[2]

# Input resumes
INPUT_DIRECTORY = BASE_DIR / "data" / "resumes" / "raw"

# Extracted JSON files
OUTPUT_DIRECTORY = BASE_DIR / "data" / "resumes" / "extracted"


def main():

    print("=" * 60)
    print("ZECPATH - RESUME TEXT EXTRACTION ENGINE")
    print("=" * 60)

    print(f"\nInput folder : {INPUT_DIRECTORY}")
    print(f"Output folder: {OUTPUT_DIRECTORY}\n")

    # Process all PDF and DOCX files
    results = process_resume_folder(
        str(INPUT_DIRECTORY),
        str(OUTPUT_DIRECTORY)
    )

    print("\n" + "=" * 60)
    print("PROCESSING SUMMARY")
    print("=" * 60)

    total = len(results)

    passed = sum(
        1
        for result in results
        if result["status"] == "PASS"
    )

    failed = sum(
        1
        for result in results
        if result["status"] == "FAIL"
    )

    print(f"Total resumes : {total}")
    print(f"Passed        : {passed}")
    print(f"Failed        : {failed}")

    print("=" * 60)


if __name__ == "__main__":
    main()