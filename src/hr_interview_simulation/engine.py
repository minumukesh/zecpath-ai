import json
from pathlib import Path
from datetime import datetime, timezone


SCORE_WEIGHTS = {
    "answer_relevance": 0.35,
    "communication": 0.20,
    "problem_solving": 0.25,
    "consistency": 0.20,
}


def validate_score(value, field_name="score"):
    """Validate a numeric score between 0 and 100."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be numeric.")

    value = float(value)

    if not 0 <= value <= 100:
        raise ValueError(f"{field_name} must be between 0 and 100.")

    return round(value, 2)


def normalize_scores(scores):
    """Validate score components and normalize weights if needed."""
    if not isinstance(scores, dict):
        raise ValueError("scores must be a dictionary.")

    required = set(SCORE_WEIGHTS)

    if set(scores) != required:
        raise ValueError(
            "Scores must contain answer_relevance, communication, "
            "problem_solving, and consistency."
        )

    return {
        name: validate_score(value, name)
        for name, value in scores.items()
    }


def calculate_weighted_score(scores):
    """Calculate a transparent weighted interview score."""
    validated = normalize_scores(scores)

    final_score = sum(
        validated[name] * SCORE_WEIGHTS[name]
        for name in SCORE_WEIGHTS
    )

    return round(final_score, 2)


def classify_performance(score):
    """Provide a simple performance category."""
    score = validate_score(score)

    if score >= 85:
        return "STRONG"
    if score >= 70:
        return "GOOD"
    if score >= 50:
        return "MODERATE"
    return "NEEDS_REVIEW"


def evaluate_candidate(candidate):
    """
    Run a reproducible simulation using the supplied assessment scores.

    This prototype uses explicit input scores. It does not infer a
    candidate's personality, experience, or ability from a real interview.
    """
    if not isinstance(candidate, dict):
        raise ValueError("Candidate must be a dictionary.")

    candidate_id = str(candidate.get("candidate_id", "")).strip()
    candidate_type = str(candidate.get("candidate_type", "")).strip().upper()

    if not candidate_id:
        raise ValueError("candidate_id cannot be empty.")

    allowed_types = {
        "CONFIDENT",
        "HESITANT",
        "INEXPERIENCED",
        "OVERQUALIFIED",
    }

    if candidate_type not in allowed_types:
        raise ValueError(
            f"Unsupported candidate type: {candidate_type}"
        )

    scores = normalize_scores(candidate.get("scores", {}))
    ai_score = calculate_weighted_score(scores)

    return {
        "candidate_id": candidate_id,
        "candidate_name": str(candidate.get("candidate_name", "")).strip(),
        "role": str(candidate.get("role", "")).strip(),
        "candidate_type": candidate_type,
        "ai_component_scores": scores,
        "ai_final_score": ai_score,
        "ai_performance_label": classify_performance(ai_score),
        "manual_expected_score": validate_score(
            candidate.get("manual_expected_score"),
            "manual_expected_score",
        ),
        "manual_expected_decision": str(
            candidate.get("manual_expected_decision", "")
        ).strip().upper(),
        "scenario_notes": str(candidate.get("scenario_notes", "")).strip(),
    }


def compare_evaluations(result, tolerance=10.0):
    """Compare simulated AI score with the supplied manual reference."""
    if isinstance(tolerance, bool) or not isinstance(tolerance, (int, float)):
        raise ValueError("tolerance must be numeric.")

    if tolerance < 0:
        raise ValueError("tolerance cannot be negative.")

    score_difference = round(
        abs(result["ai_final_score"] - result["manual_expected_score"]),
        2,
    )

    score_consistent = score_difference <= tolerance

    manual_decision = result["manual_expected_decision"]

    allowed_decisions = {
        "STRONG",
        "GOOD",
        "MODERATE",
        "NEEDS_REVIEW",
    }

    if manual_decision not in allowed_decisions:
        raise ValueError(
            f"Unsupported manual decision: {manual_decision}"
        )

    ai_decision = result["ai_performance_label"]
    decision_consistent = ai_decision == manual_decision

    issues = []

    if not score_consistent:
        issues.append("SCORE_DIFFERENCE_EXCEEDS_TOLERANCE")

    if not decision_consistent:
        issues.append("PERFORMANCE_LABEL_MISMATCH")

    return {
        **result,
        "score_difference": score_difference,
        "score_tolerance": float(tolerance),
        "score_consistent": score_consistent,
        "decision_consistent": decision_consistent,
        "manual_decision": manual_decision,
        "evaluation_status": "CONSISTENT" if not issues else "REVIEW_REQUIRED",
        "inconsistencies": issues,
    }


def generate_recommendations(results):
    """Generate improvement recommendations from observed mismatches."""
    recommendations = []

    score_mismatches = [
        item for item in results
        if not item["score_consistent"]
    ]

    decision_mismatches = [
        item for item in results
        if not item["decision_consistent"]
    ]

    if score_mismatches:
        recommendations.append(
            "Review cases where the AI score differs from the manual "
            "reference by more than the configured tolerance."
        )

    if decision_mismatches:
        recommendations.append(
            "Review performance-label thresholds and the scoring rubric "
            "for cases where AI and manual labels disagree."
        )

    if not results:
        recommendations.append(
            "Add interview simulation cases before drawing conclusions."
        )

    if len(results) < 20:
        recommendations.append(
            "Expand the test dataset before treating the measured accuracy "
            "as representative of real-world performance."
        )

    recommendations.append(
        "Use consistent, job-related evaluation criteria across candidate "
        "types. Do not penalize candidates merely for appearing hesitant "
        "or being overqualified."
    )

    recommendations.append(
        "Have qualified reviewers validate the manual reference scores "
        "and decisions before using the evaluation in hiring."
    )

    return recommendations


def generate_test_report(candidates, tolerance=10.0):
    """Run all simulation cases and calculate comparison metrics."""
    if not isinstance(candidates, list):
        raise ValueError("candidates must be a list.")

    if not candidates:
        raise ValueError("At least one candidate is required.")

    results = []

    for candidate in candidates:
        evaluated = evaluate_candidate(candidate)
        compared = compare_evaluations(evaluated, tolerance=tolerance)
        results.append(compared)

    total = len(results)

    score_consistent_count = sum(
        item["score_consistent"] for item in results
    )

    decision_consistent_count = sum(
        item["decision_consistent"] for item in results
    )

    overall_consistent_count = sum(
        item["evaluation_status"] == "CONSISTENT"
        for item in results
    )

    score_consistency_rate = round(
        score_consistent_count / total * 100, 2
    )

    decision_accuracy = round(
        decision_consistent_count / total * 100, 2
    )

    overall_consistency_rate = round(
        overall_consistent_count / total * 100, 2
    )

    return {
        "day": 40,
        "title": "HR Interview Simulation",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_simulations": total,
        "score_tolerance": tolerance,
        "metrics": {
            "score_consistent_cases": score_consistent_count,
            "decision_consistent_cases": decision_consistent_count,
            "overall_consistent_cases": overall_consistent_count,
            "score_consistency_rate_percent": score_consistency_rate,
            "decision_accuracy_percent": decision_accuracy,
            "overall_consistency_rate_percent": overall_consistency_rate,
        },
        "results": results,
        "improvement_recommendations": generate_recommendations(results),
        "limitations": [
            "The demonstration uses supplied simulation scores, not live AI interview analysis.",
            "Manual reference decisions are assumed to be supplied and validated.",
            "The measured accuracy applies only to this test dataset.",
            "Candidate presentation style must not be treated as proof of competence.",
            "Human review is required before any real hiring decision.",
        ],
    }


def save_report(report, output_dir):
    """Save the test report in JSON and Markdown formats."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "day40_hr_interview_test_report.json"
    markdown_path = output_dir / "day40_hr_interview_test_report.md"

    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    metrics = report["metrics"]

    lines = [
        "# Day 40 - HR Interview Simulation Report",
        "",
        f"Total simulations: {report['total_simulations']}",
        f"Score consistency: {metrics['score_consistency_rate_percent']}%",
        f"Decision accuracy: {metrics['decision_accuracy_percent']}%",
        f"Overall consistency: {metrics['overall_consistency_rate_percent']}%",
        "",
        "## Candidate Results",
        "",
        "| Candidate | Type | AI Score | Manual Score | AI Decision | Manual Decision | Status |",
        "|---|---|---:|---:|---|---|---|",
    ]

    for item in report["results"]:
        lines.append(
            f"| {item['candidate_id']} "
            f"| {item['candidate_type']} "
            f"| {item['ai_final_score']:.2f} "
            f"| {item['manual_expected_score']:.2f} "
            f"| {item['ai_performance_label']} "
            f"| {item['manual_decision']} "
            f"| {item['evaluation_status']} |"
        )

    lines.extend(["", "## Scoring Inconsistencies", ""])

    mismatches = [
        item for item in report["results"]
        if item["inconsistencies"]
    ]

    if mismatches:
        for item in mismatches:
            lines.append(
                f"- {item['candidate_id']}: "
                f"{', '.join(item['inconsistencies'])}"
            )
    else:
        lines.append("- No inconsistencies detected in this sample.")

    lines.extend(["", "## Improvement Recommendations", ""])

    lines.extend(
        f"- {item}"
        for item in report["improvement_recommendations"]
    )

    lines.extend([
        "",
        "## Limitations",
        "",
    ])

    lines.extend(
        f"- {item}"
        for item in report["limitations"]
    )

    markdown_path.write_text("\n".join(lines), encoding="utf-8")

    return json_path, markdown_path
