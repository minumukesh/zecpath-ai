"""Accuracy, threshold, intent, consistency and speed optimization."""

import re
import time
from statistics import mean, pstdev

from .config import (
    DEFAULT_THRESHOLD,
    THRESHOLD_CANDIDATES,
    INTENT_KEYWORDS,
    CONSISTENCY_RANGE_LIMIT,
)


class OptimizationEngine:

    # ------------------------------------------------------
    # FALSE POSITIVE / FALSE NEGATIVE ANALYSIS
    # ------------------------------------------------------

    def evaluate_predictions(self, records, threshold):

        tp = fp = tn = fn = 0

        for record in records:

            actual = bool(record["actual_positive"])
            predicted = float(record["score"]) >= threshold

            if actual and predicted:
                tp += 1
            elif not actual and predicted:
                fp += 1
            elif not actual and not predicted:
                tn += 1
            else:
                fn += 1

        total = tp + fp + tn + fn

        accuracy = (tp + tn) / total if total else 0
        precision = tp / (tp + fp) if tp + fp else 0
        recall = tp / (tp + fn) if tp + fn else 0
        specificity = tn / (tn + fp) if tn + fp else 0

        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall else 0
        )

        balanced_accuracy = (recall + specificity) / 2

        return {
            "threshold": threshold,
            "total": total,
            "true_positives": tp,
            "false_positives": fp,
            "true_negatives": tn,
            "false_negatives": fn,
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "specificity": round(specificity, 4),
            "f1_score": round(f1, 4),
            "balanced_accuracy": round(balanced_accuracy, 4),
        }

    # ------------------------------------------------------
    # SCORING THRESHOLD OPTIMIZATION
    # ------------------------------------------------------

    def optimize_threshold(self, records):

        if not records:
            raise ValueError("Evaluation dataset cannot be empty.")

        results = []

        for threshold in THRESHOLD_CANDIDATES:

            result = self.evaluate_predictions(
                records,
                threshold
            )

            results.append(result)

        best = max(
            results,
            key=lambda item: (
                item["balanced_accuracy"],
                -(
                    item["false_positives"]
                    + item["false_negatives"]
                ),
                -abs(item["threshold"] - DEFAULT_THRESHOLD)
            )
        )

        return {
            "baseline": self.evaluate_predictions(
                records,
                DEFAULT_THRESHOLD
            ),
            "optimized": best,
            "threshold_comparison": results,
        }

    # ------------------------------------------------------
    # INTENT DETECTION REFINEMENT
    # ------------------------------------------------------

    def normalize_text(self, text):

        if not isinstance(text, str):
            raise ValueError("Intent input must be text.")

        text = text.lower().strip()

        text = re.sub(r"[^\w\s']", " ", text)

        text = re.sub(r"\s+", " ", text).strip()

        return text

    def detect_intent(self, text):

        normalized = self.normalize_text(text)

        if not normalized:
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "normalized_text": normalized,
            }

        matches = []

        padded = f" {normalized} "

        for intent, keywords in INTENT_KEYWORDS.items():

            matched = []

            for keyword in keywords:

                if f" {keyword} " in padded:
                    matched.append(keyword)

            if matched:
                matches.append({
                    "intent": intent,
                    "matches": matched,
                    "count": len(matched),
                })

        if not matches:
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "normalized_text": normalized,
            }

        matches.sort(
            key=lambda item: item["count"],
            reverse=True
        )

        # Multiple equally strong categories are ambiguous.
        if (
            len(matches) > 1
            and matches[0]["count"] == matches[1]["count"]
        ):
            return {
                "intent": "ambiguous",
                "confidence": 0.0,
                "normalized_text": normalized,
            }

        winner = matches[0]

        confidence = min(
            0.95,
            0.70 + (winner["count"] - 1) * 0.10
        )

        return {
            "intent": winner["intent"],
            "confidence": round(confidence, 2),
            "normalized_text": normalized,
        }

    def evaluate_intents(self, records):

        total = len(records)
        correct = 0
        results = []

        for record in records:

            prediction = self.detect_intent(
                record["text"]
            )

            expected = record["expected_intent"]

            is_correct = (
                prediction["intent"] == expected
            )

            if is_correct:
                correct += 1

            results.append({
                "text": record["text"],
                "expected": expected,
                "predicted": prediction["intent"],
                "confidence": prediction["confidence"],
                "correct": is_correct,
            })

        accuracy = correct / total if total else 0

        return {
            "total": total,
            "correct": correct,
            "incorrect": total - correct,
            "accuracy": round(accuracy, 4),
            "results": results,
        }

    # ------------------------------------------------------
    # CROSS-ROUND CONSISTENCY
    # ------------------------------------------------------

    def aggregate_rounds(self, round_scores):

        if not round_scores:
            raise ValueError("At least one round score is required.")

        for score in round_scores:

            if not isinstance(score, (int, float)):
                raise ValueError("Round scores must be numeric.")

            if not 0 <= score <= 100:
                raise ValueError("Round scores must be between 0 and 100.")

        average = mean(round_scores)
        minimum = min(round_scores)
        maximum = max(round_scores)
        variation = maximum - minimum

        consistent = variation <= CONSISTENCY_RANGE_LIMIT

        return {
            "round_scores": round_scores,
            "round_count": len(round_scores),
            "average_score": round(average, 2),
            "minimum_score": minimum,
            "maximum_score": maximum,
            "score_variation": round(variation, 2),
            "standard_deviation": round(
                pstdev(round_scores), 2
            ),
            "consistency_status": (
                "CONSISTENT" if consistent else "REVIEW_REQUIRED"
            ),
        }

    # ------------------------------------------------------
    # PROCESSING SPEED OPTIMIZATION
    # ------------------------------------------------------

    def benchmark_processing(self, records, iterations=1000):

        """Benchmark intent detection independently of scoring evaluation."""

        if iterations <= 0:
            raise ValueError("Iterations must be positive.")

        if not records:
            raise ValueError("Benchmark dataset cannot be empty.")

        for record in records:
            if not isinstance(record, dict) or "text" not in record:
                raise ValueError(
                    "Each benchmark record must contain a text field."
                )

        start = time.perf_counter()

        processed = 0

        for _ in range(iterations):

            for record in records:

                self.detect_intent(record["text"])

                processed += 1

        elapsed = time.perf_counter() - start

        return {
            "benchmark_type": "intent_detection",
            "iterations": iterations,
            "records_per_iteration": len(records),
            "total_operations": processed,
            "elapsed_seconds": round(elapsed, 6),
            "operations_per_second": round(
                processed / elapsed, 2
            ) if elapsed > 0 else 0,
        }

    def generate_report(
        self,
        evaluation_records,
        intent_records,
        round_scores,
        benchmark_iterations=1000
    ):

        threshold_result = self.optimize_threshold(
            evaluation_records
        )

        intent_result = self.evaluate_intents(
            intent_records
        )

        consistency_result = self.aggregate_rounds(
            round_scores
        )

        benchmark_result = self.benchmark_processing(
            intent_records,
            benchmark_iterations
        )

        return {
            "report_title": "Day 54 AI Optimization and Refinement",
            "false_positive_negative_analysis": {
                "baseline": threshold_result["baseline"],
                "optimized": threshold_result["optimized"],
            },
            "scoring_threshold_optimization": threshold_result,
            "intent_detection": intent_result,
            "cross_round_consistency": consistency_result,
            "processing_speed": benchmark_result,
            "limitations": [
                "Results depend on the quality and representativeness of the evaluation dataset.",
                "Synthetic demonstration data does not establish production accuracy.",
                "Benchmark results depend on the local hardware and runtime environment.",
                "Optimized thresholds require validation on unseen real-world data.",
            ],
        }
