import json
from pathlib import Path

from src.aptitude_logic import score_answer, save_report


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "day38" / "aptitude_samples.json"
OUTPUT_DIR = ROOT / "outputs" / "day38"


def main():
    with DATA_FILE.open("r", encoding="utf-8-sig") as file:
        samples = json.load(file)

    results = []

    print("=" * 70)
    print("DAY 38 - APTITUDE LOGIC DESIGN")
    print("=" * 70)
    print(f"Sample questions: {len(samples)}")

    for sample in samples:
        result = score_answer(
            question_id=sample["question_id"],
            question=sample["question"],
            answer=sample["answer"],
            question_type=sample["question_type"],
            reference_points=sample["reference_points"],
            reviewer_scores=sample["reviewer_scores"],
        )

        results.append(result)

        print("-" * 70)
        print(f"Question ID: {result['question_id']}")
        print(f"Question type: {result['question_type']}")
        print(f"Question: {result['question']}")
        print(
            "Reasoning score: "
            f"{result['reasoning_evaluation']['score']}/100"
        )
        print(
            "Matched reference points: "
            f"{result['reasoning_evaluation']['matched_points']}"
        )
        print(
            "Missing reference points: "
            f"{result['reasoning_evaluation']['missing_points']}"
        )
        print("Component breakdown:")

        for name, component in result["component_breakdown"].items():
            print(
                f"  {name}: score={component['score']}, "
                f"weight={component['weight']}, "
                f"contribution={component['weighted_contribution']}"
            )

        print(
            "Final aptitude score: "
            f"{result['final_aptitude_score']}/100"
        )
        print(
            "Recommended answer structure: "
            f"{result['ideal_answer_structure']}"
        )

    json_path, markdown_path = save_report(results, OUTPUT_DIR)

    print("-" * 70)
    print(f"JSON report: {json_path.relative_to(ROOT)}")
    print(f"Markdown report: {markdown_path.relative_to(ROOT)}")
    print("DAY 38 DEMO COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
