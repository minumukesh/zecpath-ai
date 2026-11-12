import math
import re
import time
import unicodedata

from .config import FILLER_WORDS, INTERVIEW_WEIGHTS


def clean_transcript(text):
    if not isinstance(text, str):
        raise ValueError("Transcript must be a string.")

    original = text

    text = unicodedata.normalize("NFKC", text)

    text = "".join(
        char for char in text
        if char.isprintable() or char in "\n\t"
    )

    text = re.sub(r"\s+", " ", text).strip()

    removed = []

    for word in FILLER_WORDS:
        pattern = r"(?i)(?<!\w)" + re.escape(word) + r"(?!\w)"
        matches = re.findall(pattern, text)

        removed.extend(matches)
        text = re.sub(pattern, "", text)

    text = re.sub(r"\s+([,.!?])", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()

    return {
        "original_transcript": original,
        "cleaned_transcript": text,
        "removed_filler_count": len(removed),
        "removed_fillers": removed
    }


def handle_follow_up(
    answer,
    previous_answer=None,
    retry_count=0,
    max_retries=2
):
    if retry_count < 0 or max_retries < 0:
        raise ValueError("Retry limits cannot be negative.")

    cleaned = clean_transcript(answer)["cleaned_transcript"]

    if not cleaned:
        trigger = "EMPTY_ANSWER"
        message = "Could you please repeat your answer?"

    elif (
        previous_answer
        and cleaned.casefold()
        == clean_transcript(previous_answer)["cleaned_transcript"].casefold()
    ):
        trigger = "REPEATED_ANSWER"
        message = "Could you provide a different example?"

    elif len(cleaned.split()) < 3:
        trigger = "INCOMPLETE_ANSWER"
        message = "Could you explain your answer in more detail?"

    else:
        return {
            "status": "ANSWER_ACCEPTED",
            "trigger": None,
            "follow_up_required": False,
            "retry_count": retry_count,
            "message": "Answer accepted."
        }

    if retry_count >= max_retries:
        return {
            "status": "REVIEW_REQUIRED",
            "trigger": trigger,
            "follow_up_required": False,
            "retry_count": retry_count,
            "message": "Retry limit reached. Human review required."
        }

    return {
        "status": "FOLLOW_UP_REQUIRED",
        "trigger": trigger,
        "follow_up_required": True,
        "retry_count": retry_count + 1,
        "message": message
    }


def validate_score(score, name="score"):
    if isinstance(score, bool):
        raise ValueError(name + " must be numeric.")

    try:
        value = float(score)
    except (TypeError, ValueError):
        raise ValueError(name + " must be numeric.")

    if not math.isfinite(value) or not 0 <= value <= 100:
        raise ValueError(name + " must be between 0 and 100.")

    return value


def calculate_refined_score(component_scores, weights=None):
    weights = weights or INTERVIEW_WEIGHTS

    if not isinstance(component_scores, dict) or not component_scores:
        raise ValueError("Component scores are required.")

    active = {}

    for name, value in component_scores.items():
        if value is not None:
            active[name] = validate_score(value, name)

    if not active:
        raise ValueError("At least one valid score is required.")

    active_weights = {}

    for name in active:
        if name not in weights:
            raise ValueError("Missing weight for " + name)

        weight = validate_score(weights[name], name + "_weight")

        active_weights[name] = weight

    total_weight = sum(active_weights.values())

    if total_weight <= 0:
        raise ValueError("Active weights must total more than zero.")

    final_score = 0.0
    breakdown = {}

    for name, score in active.items():
        normalized_weight = active_weights[name] / total_weight
        contribution = score * normalized_weight
        final_score += contribution

        breakdown[name] = {
            "score": round(score, 2),
            "normalized_weight": round(normalized_weight * 100, 2),
            "contribution": round(contribution, 2)
        }

    return {
        "final_score": round(final_score, 2),
        "component_breakdown": breakdown
    }


def classify_decision(score, threshold=70):
    score = validate_score(score)

    if score >= threshold:
        return "PASS"

    return "HOLD"


def evaluate_decisions(cases, threshold=70):
    threshold = validate_score(threshold, "threshold")

    tp = tn = fp = fn = 0
    mismatches = []

    for case in cases:
        score = validate_score(case["score"])
        expected = str(case["human_decision"]).upper()

        if expected not in ("PASS", "HOLD"):
            raise ValueError("Human decision must be PASS or HOLD.")

        predicted = classify_decision(score, threshold)

        if predicted == "PASS" and expected == "PASS":
            tp += 1
        elif predicted == "HOLD" and expected == "HOLD":
            tn += 1
        elif predicted == "PASS" and expected == "HOLD":
            fp += 1
        else:
            fn += 1

        if predicted != expected:
            mismatches.append({
                "candidate_id": case["candidate_id"],
                "predicted": predicted,
                "expected": expected,
                "score": score
            })

    total = tp + tn + fp + fn

    accuracy = (tp + tn) / total if total else 0
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    specificity = tn / (tn + fp) if tn + fp else 0

    balanced = (
        (recall + specificity) / 2
        if total and tp + fn and tn + fp
        else 0
    )

    return {
        "threshold": threshold,
        "total_cases": total,
        "true_positive": tp,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
        "accuracy": round(accuracy * 100, 2),
        "precision": round(precision * 100, 2),
        "recall": round(recall * 100, 2),
        "specificity": round(specificity * 100, 2),
        "balanced_accuracy": round(balanced * 100, 2),
        "mismatches": mismatches
    }


def optimize_threshold(cases):
    if not cases:
        raise ValueError("Evaluation cases are required.")

    results = []

    for threshold in range(50, 96, 5):
        result = evaluate_decisions(cases, threshold)

        errors = (
            result["false_positive"]
            + result["false_negative"]
        )

        results.append({
            "threshold": threshold,
            "balanced_accuracy": result["balanced_accuracy"],
            "errors": errors
        })

    best = max(
        results,
        key=lambda item: (
            item["balanced_accuracy"],
            -item["errors"],
            -abs(item["threshold"] - 70)
        )
    )

    return {
        "selected_threshold": best["threshold"],
        "threshold_comparisons": results
    }


def benchmark_processing(cases, threshold=70):
    start = time.perf_counter()

    for case in cases:
        clean_transcript(case.get("transcript", ""))
        classify_decision(case["score"], threshold)

    elapsed = time.perf_counter() - start

    return {
        "processed_cases": len(cases),
        "processing_time_seconds": round(elapsed, 6),
        "average_time_per_case": round(
            elapsed / len(cases), 6
        ) if cases else 0
    }
