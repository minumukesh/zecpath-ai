import json
from pathlib import Path

from src.day54_optimization.engine import OptimizationEngine


def main():

    dataset_path = Path("data/day54/optimization_dataset.json")

    with dataset_path.open("r", encoding="utf-8-sig") as file:
        dataset = json.load(file)

    engine = OptimizationEngine()

    print("\n==========================================")
    print(" DAY 54 - OPTIMIZATION & REFINEMENT")
    print("==========================================")

    report = engine.generate_report(
        evaluation_records=dataset["evaluation_cases"],
        intent_records=dataset["intent_cases"],
        round_scores=dataset["round_scores"],
        benchmark_iterations=1000,
    )

    fpfn = report["false_positive_negative_analysis"]

    print("\n1. FALSE POSITIVE / FALSE NEGATIVE ANALYSIS")
    print("------------------------------------------")

    print("Baseline threshold:", fpfn["baseline"]["threshold"])
    print("Baseline accuracy:", fpfn["baseline"]["accuracy"])
    print("Baseline false positives:", fpfn["baseline"]["false_positives"])
    print("Baseline false negatives:", fpfn["baseline"]["false_negatives"])

    print("\nOptimized threshold:", fpfn["optimized"]["threshold"])
    print("Optimized accuracy:", fpfn["optimized"]["accuracy"])
    print("Optimized false positives:", fpfn["optimized"]["false_positives"])
    print("Optimized false negatives:", fpfn["optimized"]["false_negatives"])
    print("Optimized F1:", fpfn["optimized"]["f1_score"])

    print("\n2. SCORING THRESHOLD OPTIMIZATION")
    print("------------------------------------------")

    for item in report["scoring_threshold_optimization"]["threshold_comparison"]:
        print(
            f"Threshold: {item['threshold']:.2f} | "
            f"Accuracy: {item['accuracy']:.2%} | "
            f"FP: {item['false_positives']} | "
            f"FN: {item['false_negatives']}"
        )

    print("\n3. INTENT DETECTION")
    print("------------------------------------------")

    intent = report["intent_detection"]

    print("Total cases:", intent["total"])
    print("Correct:", intent["correct"])
    print("Incorrect:", intent["incorrect"])
    print("Intent accuracy:", f"{intent['accuracy']:.2%}")

    for item in intent["results"]:
        print(
            f"{item['text']!r} -> "
            f"{item['predicted']} "
            f"(expected: {item['expected']})"
        )

    print("\n4. CROSS-ROUND CONSISTENCY")
    print("------------------------------------------")

    consistency = report["cross_round_consistency"]

    print("Round scores:", consistency["round_scores"])
    print("Average:", consistency["average_score"])
    print("Variation:", consistency["score_variation"])
    print("Standard deviation:", consistency["standard_deviation"])
    print("Status:", consistency["consistency_status"])

    print("\n5. PROCESSING SPEED")
    print("------------------------------------------")

    speed = report["processing_speed"]

    print("Iterations:", speed["iterations"])
    print("Total operations:", speed["total_operations"])
    print("Elapsed seconds:", speed["elapsed_seconds"])
    print("Operations per second:", speed["operations_per_second"])

    output_dir = Path("outputs/day54")
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "optimization_report.json"

    json_path.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )

    markdown = f"""# Day 54 - Optimization & Refinement Report

## Objective
Improve AI accuracy and reduce incorrect decisions.

## 1. False Positive / False Negative Analysis

| Metric | Baseline | Optimized |
|---|---:|---:|
| Threshold | {fpfn['baseline']['threshold']} | {fpfn['optimized']['threshold']} |
| Accuracy | {fpfn['baseline']['accuracy']:.2%} | {fpfn['optimized']['accuracy']:.2%} |
| False Positives | {fpfn['baseline']['false_positives']} | {fpfn['optimized']['false_positives']} |
| False Negatives | {fpfn['baseline']['false_negatives']} | {fpfn['optimized']['false_negatives']} |
| F1 Score | {fpfn['baseline']['f1_score']:.4f} | {fpfn['optimized']['f1_score']:.4f} |

## 2. Scoring Threshold Optimization

The engine evaluated multiple thresholds and selected the threshold with the best balanced accuracy, using error count and baseline proximity as tie-breakers.

## 3. Intent Detection

- Total cases: {intent['total']}
- Correct predictions: {intent['correct']}
- Incorrect predictions: {intent['incorrect']}
- Accuracy: {intent['accuracy']:.2%}

## 4. Cross-Round Consistency

- Round scores: {consistency['round_scores']}
- Average score: {consistency['average_score']}
- Score variation: {consistency['score_variation']}
- Standard deviation: {consistency['standard_deviation']}
- Status: {consistency['consistency_status']}

Consistency is checked using the configured maximum score range.

## 5. Processing Speed

- Iterations: {speed['iterations']}
- Total operations: {speed['total_operations']}
- Elapsed seconds: {speed['elapsed_seconds']}
- Operations per second: {speed['operations_per_second']}

## Limitations

This report uses a synthetic demonstration dataset. Its metrics do not establish real-world production accuracy. Thresholds must be validated against representative, independently labelled data before deployment.
"""

    md_path = output_dir / "optimization_report.md"
    md_path.write_text(markdown, encoding="utf-8")

    print("\n==========================================")
    print(" DAY 54 OPTIMIZATION COMPLETED")
    print("==========================================")
    print("JSON report:", json_path)
    print("Markdown report:", md_path)


if __name__ == "__main__":
    main()
