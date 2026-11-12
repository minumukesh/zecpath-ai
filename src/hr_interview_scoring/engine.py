import json
from pathlib import Path
from datetime import datetime, timezone


DEFAULT_WEIGHTS = {
    "answer_relevance": 0.40,
    "communication": 0.25,
    "confidence": 0.20,
    "consistency": 0.15,
}


def validate_weights(weights):
    """Validate configurable scoring weights."""
    required = set(DEFAULT_WEIGHTS)

    if not isinstance(weights, dict):
        raise ValueError("Weights must be a dictionary.")

    if set(weights) != required:
        raise ValueError(
            "Weights must contain answer_relevance, communication, "
            "confidence, and consistency."
        )

    validated = {}

    for name, value in weights.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"Weight '{name}' must be numeric.")

        if value < 0:
            raise ValueError(f"Weight '{name}' cannot be negative.")

        validated[name] = float(value)

    total = sum(validated.values())

    if total <= 0:
        raise ValueError("At least one weight must be positive.")

    return {
        name: value / total
        for name, value in validated.items()
    }


def validate_score(value, field_name):
    """Validate an individual score on a 0-100 scale."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be a number from 0 to 100.")

    value = float(value)

    if not 0 <= value <= 100:
        raise ValueError(f"{field_name} must be between 0 and 100.")

    return value


def normalize_interview_scores(questions):
    """
    Normalize question scores so interviews with different numbers
    of questions can be compared on the same 0-100 scale.
    """
    if not isinstance(questions, list) or not questions:
        raise ValueError("At least one scored interview question is required.")

    normalized_questions = []

    for index, question in enumerate(questions, start=1):
        if not isinstance(question, dict):
            raise ValueError("Each question must be a dictionary.")

        question_id = question.get("question_id", f"Q{index}")
        question_text = str(question.get("question", "")).strip()
        answer = str(question.get("answer", "")).strip()

        if not question_text:
            raise ValueError(
                f"Question {question_id} must include question text."
            )

        relevance = validate_score(
            question.get("answer_relevance", 0),
            "answer_relevance",
        )

        normalized_questions.append({
            "question_id": str(question_id),
            "question": question_text,
            "answer": answer,
            "answer_relevance": relevance,
        })

    # Each question is scored on the same 0-100 scale.
    # Averaging keeps the overall relevance score independent
    # of the number of questions.
    relevance_scores = [
        question["answer_relevance"]
        for question in normalized_questions
    ]

    average_relevance = sum(relevance_scores) / len(relevance_scores)

    return {
        "questions": normalized_questions,
        "question_count": len(normalized_questions),
        "average_answer_relevance": round(average_relevance, 2),
        "normalization_method": "Arithmetic mean of question scores (0-100)",
    }


def classify_interview_score(score):
    """Provide an explanatory score band, not an automatic hiring decision."""
    if score >= 85:
        return "HIGH_SCORE"
    if score >= 70:
        return "GOOD_SCORE"
    if score >= 50:
        return "MODERATE_SCORE"
    return "LOW_SCORE"


def score_hr_interview(
    candidate_id,
    candidate_name,
    role,
    questions,
    communication_score,
    confidence_score,
    consistency_score,
    weights=None,
):
    """
    Combine answer relevance, communication, confidence signals,
    and consistency into an explainable 0-100 prototype score.
    """
    if not str(candidate_id).strip():
        raise ValueError("candidate_id cannot be empty.")

    if not str(candidate_name).strip():
        raise ValueError("candidate_name cannot be empty.")

    if not str(role).strip():
        raise ValueError("role cannot be empty.")

    communication_score = validate_score(
        communication_score, "communication_score"
    )
    confidence_score = validate_score(
        confidence_score, "confidence_score"
    )
    consistency_score = validate_score(
        consistency_score, "consistency_score"
    )

    active_weights = validate_weights(
        weights if weights is not None else DEFAULT_WEIGHTS
    )

    normalized = normalize_interview_scores(questions)

    component_scores = {
        "answer_relevance": normalized["average_answer_relevance"],
        "communication": communication_score,
        "confidence": confidence_score,
        "consistency": consistency_score,
    }

    weighted_breakdown = {}

    for component, score in component_scores.items():
        weight = active_weights[component]

        weighted_breakdown[component] = {
            "score": round(score, 2),
            "weight": round(weight, 4),
            "weighted_contribution": round(score * weight, 2),
        }

    final_score = sum(
        item["weighted_contribution"]
        for item in weighted_breakdown.values()
    )

    final_score = round(max(0.0, min(100.0, final_score)), 2)

    explanations = {
        "answer_relevance": (
            "Average relevance score across the interview questions."
        ),
        "communication": (
            "Communication score supplied by the configured evaluation "
            "process."
        ),
        "confidence": (
            "Confidence signal score supplied by the confidence analyzer. "
            "It is not proof of actual confidence."
        ),
        "consistency": (
            "Consistency score supplied by the evaluation process."
        ),
    }

    return {
        "candidate_id": str(candidate_id),
        "candidate_name": str(candidate_name),
        "role": str(role),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "question_count": normalized["question_count"],
        "normalization": normalized["normalization_method"],
        "component_scores": component_scores,
        "weights": {
            name: round(value, 4)
            for name, value in active_weights.items()
        },
        "weighted_breakdown": weighted_breakdown,
        "final_hr_interview_score": final_score,
        "score_range": "0-100",
        "score_classification": classify_interview_score(final_score),
        "explanations": explanations,
        "question_breakdown": normalized["questions"],
        "limitations": [
            "This is a prototype scoring framework, not a validated hiring model.",
            "Input component scores depend on the methods used to generate them.",
            "Text-based confidence indicators cannot reliably determine actual confidence.",
            "The final score must support human review, not replace recruiter judgment.",
        ],
    }


def save_interview_report(results, output_dir):
    """Save candidate results in JSON and recruiter-friendly Markdown."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "day37_hr_interview_report.json"
    markdown_path = output_dir / "day37_hr_interview_report.md"

    report = {
        "day": 37,
        "title": "HR Interview Scoring Engine",
        "total_candidates": len(results),
        "scoring_weights": results[0]["weights"] if results else {},
        "results": results,
    }

    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "# Day 37 - HR Interview Scoring Report",
        "",
        f"Candidates evaluated: {len(results)}",
        "",
        "## Score Summary",
        "",
        "| Candidate ID | Candidate | Role | Relevance | Communication | Confidence | Consistency | Final Score |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]

    for result in results:
        scores = result["component_scores"]

        lines.append(
            f"| {result['candidate_id']} "
            f"| {result['candidate_name']} "
            f"| {result['role']} "
            f"| {scores['answer_relevance']:.2f} "
            f"| {scores['communication']:.2f} "
            f"| {scores['confidence']:.2f} "
            f"| {scores['consistency']:.2f} "
            f"| {result['final_hr_interview_score']:.2f} |"
        )

    lines.extend([
        "",
        "## Scoring Formula",
        "",
        "Final Score = Relevance × Relevance Weight",
        "+ Communication × Communication Weight",
        "+ Confidence × Confidence Weight",
        "+ Consistency × Consistency Weight",
        "",
        "All component scores use a 0-100 scale.",
        "Weights are normalized to sum to 1.",
        "",
        "## Interpretation",
        "",
        "The score is an explainable prototype result and should be reviewed",
        "alongside interview evidence by a human recruiter.",
        "",
        "## Limitations",
        "",
    ])

    for limitation in (
        results[0]["limitations"] if results else []
    ):
        lines.append(f"- {limitation}")

    lines.append("")

    markdown_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return json_path, markdown_path
