import json
from pathlib import Path

from src.confidence_stress import analyze_response, save_report


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "day36" / "confidence_stress_samples.json"
OUTPUT_DIR = ROOT / "outputs" / "day36"


def main():
    with DATA_FILE.open("r", encoding="utf-8-sig") as file:
        samples = json.load(file)

    results = []

    print("=" * 68)
    print("DAY 36 - CONFIDENCE & STRESS INDICATORS")
    print("=" * 68)
    print(f"Sample responses: {len(samples)}")

    for sample in samples:
        result = analyze_response(
            sample["response_id"],
            sample["text"],
        )

        results.append(result)

        print("-" * 68)
        print(f"Response: {sample['response_id']}")
        print(f"Scenario: {sample['scenario']}")
        print(
            "Hesitation words: "
            f"{result['hesitation_analysis']['hesitation_word_count']}"
        )
        print(
            "Uncertainty phrases: "
            f"{result['hesitation_analysis']['uncertainty_phrases']}"
        )
        print(
            "Repeated words: "
            f"{result['hesitation_analysis']['repeated_word_count']}"
        )
        print(
            "Long pauses: "
            f"{result['hesitation_analysis']['long_pause_count']}"
        )
        print(
            "Sentiment wording: "
            f"{result['sentiment_analysis']['label']}"
        )
        print(
            "Potential contradictions: "
            f"{result['contradiction_analysis']['potential_contradiction_count']}"
        )
        print(
            "Stress indicators: "
            f"{result['stress_analysis']['indicator_level']}"
        )
        print(
            "Behavioral confidence signal score: "
            f"{result['behavioral_confidence']['score']}/100"
        )

    json_path, markdown_path = save_report(results, OUTPUT_DIR)

    print("-" * 68)
    print(f"JSON report: {json_path.relative_to(ROOT)}")
    print(f"Markdown report: {markdown_path.relative_to(ROOT)}")
    print("DAY 36 DEMO COMPLETED")
    print("=" * 68)


if __name__ == "__main__":
    main()
