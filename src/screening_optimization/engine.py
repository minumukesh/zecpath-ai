import re
from typing import Any


INTENT_KEYWORDS = {
    "skills": [
        "python", "sql", "excel", "power bi", "tableau",
        "communication", "programming", "analytics",
        "machine learning", "java", "javascript", "coding",
        "tools", "skills", "technology",
    ],
    "experience": [
        "experience", "worked", "work", "internship",
        "project", "projects", "company", "years",
        "responsibilities", "developed", "managed",
    ],
    "availability": [
        "available", "join", "joining", "notice period",
        "immediately", "days", "weeks", "months",
        "start date",
    ],
    "salary": [
        "salary", "expected pay", "compensation",
        "stipend", "remuneration", "lpa", "per annum",
        "package",
    ],
    "education": [
        "degree", "bachelor", "master", "mca", "bca",
        "bsc", "b.com", "mba", "college", "university",
        "graduated", "education", "qualification",
    ],
    "introduction": [
        "my name", "i am", "i'm", "myself",
        "introduce", "introduction", "background",
    ],
}

UNCERTAINTY_PHRASES = [
    "not sure",
    "i don't know",
    "i do not know",
    "maybe",
    "i am confused",
    "i'm confused",
    "i don't understand",
    "i do not understand",
    "can you repeat",
    "please explain",
]


def normalize_text(text: Any) -> str:
    """Normalize a candidate response for consistent processing."""
    if text is None:
        return ""

    text = str(text).strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def detect_intent(answer: str) -> dict:
    """Classify the likely intent of a candidate's response."""
    normalized = normalize_text(answer)
    words = normalized.split()

    if not normalized or len(words) < 2:
        return {
            "intent": "unclear",
            "confidence": 0.95 if not normalized else 0.75,
            "matched_keywords": [],
            "reason": "The response is empty or too short.",
        }

    for phrase in UNCERTAINTY_PHRASES:
        if phrase in normalized:
            return {
                "intent": "unclear",
                "confidence": 0.90,
                "matched_keywords": [phrase],
                "reason": "An uncertainty or confusion phrase was detected.",
            }

    matches = {}

    for intent, keywords in INTENT_KEYWORDS.items():
        found = [
            keyword for keyword in keywords
            if keyword in normalized
        ]

        if found:
            matches[intent] = found

    if not matches:
        return {
            "intent": "off_topic",
            "confidence": 0.80,
            "matched_keywords": [],
            "reason": "No recognized screening-related keywords were found.",
        }

    # Use the intent with the greatest number of matched keywords.
    # In a tie, use the order in which the categories are defined.
    selected_intent = max(
        matches,
        key=lambda intent: len(matches[intent]),
    )

    selected_matches = matches[selected_intent]

    confidence = min(
        0.99,
        0.60 + 0.12 * len(selected_matches),
    )

    return {
        "intent": selected_intent,
        "confidence": round(confidence, 2),
        "matched_keywords": selected_matches,
        "reason": (
            f"Matched {len(selected_matches)} keyword(s) "
            f"associated with {selected_intent}."
        ),
    }


def score_response(answer: str, expected_intent: str) -> dict:
    """
    Calculate an explainable screening score.

    This is a rule-based prototype, not a trained AI model.
    """
    normalized = normalize_text(answer)
    words = normalized.split()
    word_count = len(words)

    if word_count == 0:
        clarity = 0
        relevance = 0
        completeness = 0
        consistency = 0

    else:
        # Clarity: estimate whether the response has enough content.
        if word_count <= 2:
            clarity = 35
        elif word_count <= 6:
            clarity = 60
        elif word_count <= 12:
            clarity = 80
        else:
            clarity = 95

        # Relevance: compare the response with the expected category.
        keywords = INTENT_KEYWORDS.get(expected_intent, [])

        matched = [
            keyword for keyword in keywords
            if keyword in normalized
        ]

        if not matched:
            relevance = 20
        elif len(matched) == 1:
            relevance = 65
        else:
            relevance = min(100, 75 + 10 * (len(matched) - 1))

        # Completeness: use response length as a simple proxy.
        if word_count <= 2:
            completeness = 25
        elif word_count <= 5:
            completeness = 45
        elif word_count <= 10:
            completeness = 70
        elif word_count <= 18:
            completeness = 85
        else:
            completeness = 95

        # Consistency: flag obvious uncertainty and contradictory cues.
        has_uncertainty = any(
            phrase in normalized
            for phrase in UNCERTAINTY_PHRASES
        )

        has_yes = bool(re.search(r"\b(yes|available|can)\b", normalized))
        has_no = bool(re.search(r"\b(no|unavailable|cannot)\b", normalized))

        if has_uncertainty:
            consistency = 40
        elif has_yes and has_no:
            consistency = 45
        else:
            consistency = 90

    total = (
        clarity * 0.25
        + relevance * 0.35
        + completeness * 0.25
        + consistency * 0.15
    )

    return {
        "clarity": round(clarity, 2),
        "relevance": round(relevance, 2),
        "completeness": round(completeness, 2),
        "consistency": round(consistency, 2),
        "total_score": round(total, 2),
        "weights": {
            "clarity": 0.25,
            "relevance": 0.35,
            "completeness": 0.25,
            "consistency": 0.15,
        },
        "explanation": (
            "The score combines clarity (25%), relevance (35%), "
            "completeness (25%), and consistency (15%)."
        ),
    }


def classify_screening_score(
    score: float,
    accept_threshold: float = 60.0,
    review_threshold: float = 35.0,
) -> str:
    """Classify a screening score as ACCEPT, REVIEW, or REJECT."""
    if not 0 <= accept_threshold <= 100:
        raise ValueError("Accept threshold must be between 0 and 100.")

    if not 0 <= review_threshold <= 100:
        raise ValueError("Review threshold must be between 0 and 100.")

    if review_threshold > accept_threshold:
        raise ValueError(
            "Review threshold cannot exceed the accept threshold."
        )

    if score >= accept_threshold:
        return "ACCEPT"

    if score >= review_threshold:
        return "REVIEW"

    return "REJECT"


def evaluate_case(
    case: dict,
    accept_threshold: float = 60.0,
    review_threshold: float = 35.0,
) -> dict:
    """Evaluate one simulated screening response."""
    answer = case["answer"]
    expected_intent = case["expected_intent"]

    intent_result = detect_intent(answer)
    score_result = score_response(answer, expected_intent)

    decision = classify_screening_score(
        score_result["total_score"],
        accept_threshold=accept_threshold,
        review_threshold=review_threshold,
    )

    human_decision = case["human_decision"]

    return {
        "candidate_id": case["candidate_id"],
        "question": case["question"],
        "answer": answer,
        "expected_intent": expected_intent,
        "detected_intent": intent_result["intent"],
        "intent_correct": (
            intent_result["intent"] == expected_intent
        ),
        "intent_confidence": intent_result["confidence"],
        "intent_reason": intent_result["reason"],
        "matched_keywords": intent_result["matched_keywords"],
        "score_breakdown": score_result,
        "ai_decision": decision,
        "human_decision": human_decision,
        "decision_match": decision == human_decision,
        "false_rejection": (
            human_decision == "ACCEPT"
            and decision == "REJECT"
        ),
        "false_acceptance": (
            human_decision == "REJECT"
            and decision == "ACCEPT"
        ),
    }


def calculate_metrics(results: list) -> dict:
    """Compare AI decisions against the predefined human decisions."""
    accepted_human = [
        result for result in results
        if result["human_decision"] == "ACCEPT"
    ]

    rejected_human = [
        result for result in results
        if result["human_decision"] == "REJECT"
    ]

    false_rejections = sum(
        result["false_rejection"] for result in results
    )

    false_acceptances = sum(
        result["false_acceptance"] for result in results
    )

    correct_decisions = sum(
        result["decision_match"] for result in results
    )

    total = len(results)

    return {
        "total_cases": total,
        "correct_decisions": correct_decisions,
        "decision_accuracy": round(
            correct_decisions / total if total else 0,
            4,
        ),
        "human_accept_cases": len(accepted_human),
        "human_reject_cases": len(rejected_human),
        "false_rejections": false_rejections,
        "false_acceptances": false_acceptances,
        "intent_correct": sum(
            result["intent_correct"] for result in results
        ),
        "intent_accuracy": round(
            sum(result["intent_correct"] for result in results) / total
            if total else 0,
            4,
        ),
        "false_rejection_rate": round(
            false_rejections / len(accepted_human)
            if accepted_human else 0,
            4,
        ),
    }


def optimize_thresholds(cases: list) -> dict:
    """
    Search candidate thresholds using labeled sample cases.

    False rejections receive a higher penalty than false acceptances.
    This is a small-data demonstration, not production calibration.
    """
    candidates = []

    for accept_threshold in range(35, 81, 5):
        review_threshold = min(35, accept_threshold)

        results = [
            evaluate_case(
                case,
                accept_threshold=accept_threshold,
                review_threshold=review_threshold,
            )
            for case in cases
        ]

        metrics = calculate_metrics(results)

        cost = (
            2 * metrics["false_rejections"]
            + metrics["false_acceptances"]
        )

        candidates.append({
            "accept_threshold": accept_threshold,
            "review_threshold": review_threshold,
            "weighted_error_cost": cost,
            "false_rejections": metrics["false_rejections"],
            "false_acceptances": metrics["false_acceptances"],
            "decision_accuracy": metrics["decision_accuracy"],
        })

    # Choose the lowest weighted error cost.
    # If costs tie, prefer fewer false rejections.
    best = min(
        candidates,
        key=lambda item: (
            item["weighted_error_cost"],
            item["false_rejections"],
            -item["accept_threshold"],
        ),
    )

    return {
        "method": (
            "Grid search on the supplied labeled sample cases; "
            "false rejections are weighted twice as heavily "
            "as false acceptances."
        ),
        "selected_accept_threshold": best["accept_threshold"],
        "selected_review_threshold": best["review_threshold"],
        "selected_weighted_error_cost": best["weighted_error_cost"],
        "candidate_results": candidates,
        "warning": (
            "Thresholds are tuned on a small demonstration dataset. "
            "Validate them on a larger independent dataset before "
            "using them for real hiring decisions."
        ),
    }


def run_evaluation(cases: list) -> dict:
    """Run baseline evaluation, tune thresholds, and evaluate again."""
    baseline_threshold = 60.0
    review_threshold = 35.0

    baseline_results = [
        evaluate_case(
            case,
            accept_threshold=baseline_threshold,
            review_threshold=review_threshold,
        )
        for case in cases
    ]

    baseline_metrics = calculate_metrics(baseline_results)
    optimization = optimize_thresholds(cases)

    optimized_results = [
        evaluate_case(
            case,
            accept_threshold=optimization["selected_accept_threshold"],
            review_threshold=optimization["selected_review_threshold"],
        )
        for case in cases
    ]

    optimized_metrics = calculate_metrics(optimized_results)

    return {
        "project": "Zecpath AI",
        "day": 30,
        "title": "Screening System Testing and Optimization",
        "evaluation_type": "Simulated screening evaluation",
        "baseline_thresholds": {
            "accept": baseline_threshold,
            "review": review_threshold,
        },
        "baseline_metrics": baseline_metrics,
        "optimization": optimization,
        "optimized_metrics": optimized_metrics,
        "results": optimized_results,
        "limitations": [
            "The dataset contains simulated responses.",
            "Human decisions are predefined evaluation labels.",
            "Intent detection and scoring use transparent rules.",
            "This evaluation does not establish real-world hiring accuracy.",
            "A human recruiter must review borderline or uncertain cases.",
        ],
    }
