import json
from pathlib import Path

from src.communication_evaluation import (
    evaluate_communication,
    save_evaluation_report,
)


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "day35" / "communication_test_samples.json"
OUTPUT_DIR = ROOT / "outputs" / "day35"


def main():
    with DATA_FILE.open("r", encoding="utf-8-sig") as file:
        samples = json.load(file)

    print("=" * 68)
    print("DAY 35 - COMMUNICATION SKILL EVALUATION")
    print("=" * 68)

    summary = []

    for sample in samples:
        result = evaluate_communication(sample["text"])
        result["evaluation_id"] = sample["sample_id"]

        json_path, markdown_path = save_evaluation_report(
            result,
            OUTPUT_DIR,
            sample["sample_id"],
        )

        summary.append({
            "sample_id": sample["sample_id"],
            "description": sample["description"],
            "communication_score": result["communication_score"],
            "word_count": result["word_count"],
            "filler_count": result["filler_word_analysis"]["count"],
            "component_scores": result["component_scores"],
        })

        print("-" * 68)
        print(f"Sample: {sample['sample_id']}")
        print(f"Description: {sample['description']}")
        print(f"Words: {result['word_count']}")
        print(f"Sentences: {result['sentence_count']}")
        print(f"Communication score: {result['communication_score']}/100")
        print(f"Component scores: {result['component_scores']}")
        print(f"Filler words: {result['filler_word_analysis']['count']}")

    summary_path = OUTPUT_DIR / "day35_summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("-" * 68)
    print(f"Summary report: {summary_path.relative_to(ROOT)}")
    print("Detailed reports: outputs/day35/")
    print("Scoring formula: docs/day35/day35_scoring_formula.md")
    print("DAY 35 DEMO COMPLETED")
    print("=" * 68)


if __name__ == "__main__":
    main()
