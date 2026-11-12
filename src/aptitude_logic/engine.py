import json
import re
from pathlib import Path
from datetime import datetime, timezone


DEFAULT_WEIGHTS = {
    "reasoning": 0.35,
    "approach": 0.25,
    "problem_solving": 0.25,
    "clarity": 0.15,
}


# These phrases are configurable indicators, not proof of reasoning ability.
APPROACH_INDICATORS = {
    "first", "then", "because", "therefore", "next",
    "step", "steps", "analyze", "check", "compare",
    "identify", "investigate", "test", "verify",
}

PROBLEM_SOLVING_INDICATORS = {
    "solution", "solve", "resolve", "debug", "test",
    "improve", "alternative", "option", "implement",
    "evaluate", "compare", "measure", "review",
}

CLARITY_INDICATORS = {
    "because", "therefore", "for example", "first",
    "next", "finally", "as a result", "the reason",
}


def normalize_text(text):
    """Normalize whitespace in a question or answer."""
    if text is None:
        return ""

    return re.sub(r"\s+", " ", str(text)).strip()


def validate_weights(weights=None):
    """Validate and normalize aptitude scoring weights."""
    if weights is None:
        weights = DEFAULT_WEIGHTS

    required = set(DEFAULT_WEIGHTS)

    if not isinstance(weights, dict) or set(weights) != required:
        raise ValueError(
            "Weights must contain reasoning, approach, "
            "problem_solving, and clarity."
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
        raise ValueError("At least one scoring weight must be positive.")

    return {
        name: value / total
        for name, value in validated.items()
    }


def validate_score(value, field_name="score"):
    """Validate a score on a 0-100 scale."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be numeric.")

    value = float(value)

    if not 0 <= value <= 100:
        raise ValueError(f"{field_name} must be between 0 and 100.")

    return value


def count_indicators(text, indicators):
    """Count distinct predefined indicators found in text."""
    normalized = normalize_text(text).lower()

    found = []

    for phrase in sorted(indicators, key=len, reverse=True):
        pattern = r"\b" + re.escape(phrase) + r"\b"

        if re.search(pattern, normalized):
            found.append(phrase)

    return found


def map_ideal_answer_structure(question_type):
    """
    Return a recommended answer structure for each question type.
    """
    structures = {
        "reasoning": [
            "Understand the problem",
            "Explain the reasoning",
            "Show the steps",
            "State the conclusion",
        ],
        "situational": [
            "Describe the situation",
            "Explain the action",
            "Give the reason",
            "Describe the expected outcome",
        ],
        "problem_solving": [
            "Identify the problem",
            "Investigate the cause",
            "Compare possible solutions",
            "Explain the selected solution",
            "Describe how the result would be checked",
        ],
    }

    key = str(question_type).strip().lower()

    if key not in structures:
        raise ValueError(
            "question_type must be reasoning, situational, "
            "or problem_solving."
        )

    return {
        "question_type": key,
        "recommended_steps": structures[key],
    }


def detect_problem_solving_clarity(answer):
    """
    Identify structural indicators in an answer.

    This checks wording patterns only. It does not prove that the
    answer is correct or that the candidate has strong reasoning.
    """
    normalized = normalize_text(answer)
    words = re.findall(r"\b[\w'-]+\b", normalized.lower())

    approach_found = count_indicators(
        normalized, APPROACH_INDICATORS
    )
    solution_found = count_indicators(
        normalized, PROBLEM_SOLVING_INDICATORS
    )
    clarity_found = count_indicators(
        normalized, CLARITY_INDICATORS
    )

    has_explanation = any(
        marker in normalized.lower()
        for marker in ("because", "the reason", "therefore")
    )

    has_example = "for example" in normalized.lower()

    has_sequence = any(
        marker in normalized.lower()
        for marker in ("first", "next", "then", "finally")
    )

    return {
        "word_count": len(words),
        "approach_indicators": approach_found,
        "problem_solving_indicators": solution_found,
        "clarity_indicators": clarity_found,
        "has_explanation_marker": has_explanation,
        "has_example_marker": has_example,
        "has_step_sequence_marker": has_sequence,
        "note": (
            "These are language-structure indicators, not a judgment "
            "of intelligence or proof that a proposed solution is correct."
        ),
    }


def evaluate_reasoning(question, answer, reference_points=None):
    """
    Calculate a transparent prototype reasoning score.

    Optional reference_points are reviewer-defined criteria supplied
    with the question. Each matched point contributes equally.
    """
    normalized_answer = normalize_text(answer)

    if not normalized_answer:
        return {
            "score": 0.0,
            "matched_points": [],
            "missing_points": list(reference_points or []),
            "explanation": "No answer was provided.",
        }

    if reference_points is None:
        reference_points = []

    if not isinstance(reference_points, list):
        raise ValueError("reference_points must be a list.")

    answer_lower = normalized_answer.lower()

    matched = [
        point for point in reference_points
        if str(point).strip()
        and str(point).lower() in answer_lower
    ]

    missing = [
        point for point in reference_points
        if str(point).strip()
        and str(point).lower() not in answer_lower
    ]

    if reference_points:
        score = 100.0 * len(matched) / len(reference_points)
        explanation = (
            "Score based on the proportion of supplied reference points "
            "matched in the answer."
        )
    else:
        # No reference criteria were supplied. Avoid inventing a factual
        # correctness score. Return a neutral, explicitly limited baseline.
        score = 50.0
        explanation = (
            "No reference criteria were supplied. A neutral baseline is "
            "used; this is not an assessment of answer correctness."
        )

    return {
        "score": round(score, 2),
        "matched_points": matched,
        "missing_points": missing,
        "explanation": explanation,
    }


def score_answer(
    question_id,
    question,
    answer,
    question_type="reasoning",
    reference_points=None,
    reviewer_scores=None,
    weights=None,
):
    """
    Score a reasoning or situational answer and return an explainable
    component breakdown.

    Reviewer scores can be supplied for reasoning, approach,
    problem_solving, and clarity. If omitted, only the reasoning
    baseline and text indicators are available. Text indicators alone
    are not a validated measure of ability.
    """
    normalized_question = normalize_text(question)
    normalized_answer = normalize_text(answer)

    if not str(question_id).strip():
        raise ValueError("question_id cannot be empty.")

    if not normalized_question:
        raise ValueError("Question text cannot be empty.")

    if not normalized_answer:
        raise ValueError("Answer text cannot be empty.")

    structure = map_ideal_answer_structure(question_type)
    clarity = detect_problem_solving_clarity(normalized_answer)

    reasoning_result = evaluate_reasoning(
        normalized_question,
        normalized_answer,
        reference_points=reference_points,
    )

    if reviewer_scores is None:
        reviewer_scores = {
            "reasoning": reasoning_result["score"],
            "approach": 50.0,
            "problem_solving": 50.0,
            "clarity": 50.0,
        }

        scoring_source = (
            "Reference-point reasoning plus neutral baselines for "
            "unreviewed dimensions."
        )
    else:
        required = set(DEFAULT_WEIGHTS)

        if not isinstance(reviewer_scores, dict):
            raise ValueError("reviewer_scores must be a dictionary.")

        if set(reviewer_scores) != required:
            raise ValueError(
                "reviewer_scores must contain reasoning, approach, "
                "problem_solving, and clarity."
            )

        reviewer_scores = {
            key: validate_score(value, key)
            for key, value in reviewer_scores.items()
        }

        scoring_source = "Supplied reviewer scores."

    active_weights = validate_weights(weights)

    breakdown = {}

    for component, component_score in reviewer_scores.items():
        weight = active_weights[component]

        breakdown[component] = {
            "score": round(component_score, 2),
            "weight": round(weight, 4),
            "weighted_contribution": round(
                component_score * weight, 2
            ),
        }

    final_score = round(
        sum(
            item["weighted_contribution"]
            for item in breakdown.values()
        ),
        2,
    )

    return {
        "question_id": str(question_id),
        "question": normalized_question,
        "answer": normalized_answer,
        "question_type": str(question_type).lower(),
        "ideal_answer_structure": structure["recommended_steps"],
        "reasoning_evaluation": reasoning_result,
        "problem_solving_clarity": clarity,
        "component_breakdown": breakdown,
        "weights": {
            name: round(value, 4)
            for name, value in active_weights.items()
        },
        "final_aptitude_score": max(0.0, min(100.0, final_score)),
        "score_range": "0-100",
        "scoring_source": scoring_source,
        "limitations": [
            "This is a prototype scoring framework.",
            "Text indicators do not establish intelligence or ability.",
            "Reference points must be reviewed for correctness and fairness.",
            "Human review is required before interpreting the result.",
        ],
    }


def evaluate_scenario(scenario_id, situation, response, reference_points=None):
    """Evaluate a situational judgment response."""
    result = score_answer(
        question_id=scenario_id,
        question=situation,
        answer=response,
        question_type="situational",
        reference_points=reference_points,
    )

    result["evaluation_type"] = "SITUATIONAL_JUDGMENT"

    return result


def save_report(results, output_dir):
    """Save aptitude evaluation results as JSON and Markdown."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "day38_aptitude_report.json"
    markdown_path = output_dir / "day38_aptitude_report.md"

    report = {
        "day": 38,
        "title": "Aptitude Logic Design",
        "total_evaluations": len(results),
        "default_weights": {
            name: round(value, 4)
            for name, value in validate_weights().items()
        },
        "results": results,
    }

    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "# Day 38 - Aptitude Logic Report",
        "",
        f"Evaluations: {len(results)}",
        "",
        "| Question ID | Type | Reasoning Score | Final Score |",
        "|---|---|---:|---:|",
    ]

    for result in results:
        lines.append(
            f"| {result['question_id']} "
            f"| {result['question_type']} "
            f"| {result['reasoning_evaluation']['score']:.2f} "
            f"| {result['final_aptitude_score']:.2f} |"
        )

    lines.extend([
        "",
        "## Workflow",
        "",
        "Question and Answer -> Ideal Structure -> Reasoning Evaluation "
        "-> Problem-Solving Indicators -> Weighted Score -> Report",
        "",
        "## Important Limitations",
        "",
        "- This prototype does not prove intelligence or ability.",
        "- Reference points and reviewer scores require human validation.",
        "- Text indicators are not a substitute for evaluating correctness.",
        "- Results should not be used alone to make hiring decisions.",
        "",
    ])

    markdown_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return json_path, markdown_path
