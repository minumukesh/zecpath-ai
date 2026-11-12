import json
import re
from pathlib import Path
from datetime import datetime, timezone


def clean_text(value):
    """Normalize text fields."""
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def normalize_score(value, field_name="score"):
    """Validate scores on a 0-100 scale."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be numeric.")

    value = float(value)

    if not 0 <= value <= 100:
        raise ValueError(f"{field_name} must be between 0 and 100.")

    return round(value, 2)


def clean_list(values):
    """Return a list of non-empty, normalized text values."""
    if values is None:
        return []

    if not isinstance(values, list):
        raise ValueError("Expected a list of text values.")

    result = []

    for value in values:
        text = clean_text(value)

        if text:
            result.append(text)

    return result


def identify_inconsistencies(answers):
    """
    Identify possible contradictions between supplied answer records.

    This is a simple rule-based check. It does not establish that a
    candidate is dishonest or that either answer is incorrect.
    """
    if not isinstance(answers, list):
        raise ValueError("answers must be a list.")

    inconsistencies = []

    for index, first in enumerate(answers):
        for second in answers[index + 1:]:
            if not isinstance(first, dict) or not isinstance(second, dict):
                continue

            first_topic = clean_text(first.get("topic")).lower()
            second_topic = clean_text(second.get("topic")).lower()

            if not first_topic or first_topic != second_topic:
                continue

            first_value = clean_text(first.get("value")).lower()
            second_value = clean_text(second.get("value")).lower()

            if not first_value or not second_value:
                continue

            if first_value != second_value:
                inconsistencies.append({
                    "topic": first_topic,
                    "first_answer": clean_text(first.get("value")),
                    "second_answer": clean_text(second.get("value")),
                    "flag": "POSSIBLE_INCONSISTENCY",
                    "explanation": (
                        "Different answers were recorded for the same "
                        "topic. A recruiter should review the context."
                    ),
                })

    return inconsistencies


def identify_risk_flags(interview):
    """
    Collect explicit, supplied interview concerns.

    Flags are prompts for human review, not automatic rejection criteria.
    """
    flags = clean_list(interview.get("risk_flags", []))

    result = []

    for flag in flags:
        result.append({
            "flag": flag,
            "status": "REVIEW_REQUIRED",
            "explanation": (
                "This item was supplied as a risk flag and requires "
                "human review before drawing a conclusion."
            ),
        })

    return result


def identify_cultural_fit_indicators(interview):
    """
    Summarize job-related collaboration indicators supplied in the input.

    The engine does not infer cultural fit from protected characteristics
    or personal background.
    """
    indicators = clean_list(
        interview.get("collaboration_indicators", [])
    )

    return [
        {
            "indicator": item,
            "category": "JOB_RELATED_COLLABORATION",
            "status": "REVIEW_WITH_JOB_CRITERIA",
        }
        for item in indicators
    ]


def calculate_overall_performance(scores):
    """Calculate an average from available, validated interview scores."""
    if not isinstance(scores, dict):
        raise ValueError("scores must be a dictionary.")

    validated = {}

    for name, value in scores.items():
        if value is not None:
            validated[str(name)] = normalize_score(value, str(name))

    if not validated:
        return {
            "overall_score": None,
            "performance_label": "NOT_ENOUGH_DATA",
            "component_scores": {},
        }

    overall = round(sum(validated.values()) / len(validated), 2)

    if overall >= 85:
        label = "STRONG_REPORTED_PERFORMANCE"
    elif overall >= 70:
        label = "GOOD_REPORTED_PERFORMANCE"
    elif overall >= 50:
        label = "MODERATE_REPORTED_PERFORMANCE"
    else:
        label = "NEEDS_FURTHER_REVIEW"

    return {
        "overall_score": overall,
        "performance_label": label,
        "component_scores": validated,
    }


def build_strengths_and_weaknesses(interview):
    """Use the supplied evidence to build a structured summary."""
    strengths = clean_list(interview.get("strengths", []))
    weaknesses = clean_list(interview.get("weaknesses", []))

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
    }


def generate_natural_language_report(summary):
    """Generate a readable recruiter-facing report."""
    candidate = summary["candidate"]
    performance = summary["overall_performance"]
    findings = summary["findings"]

    lines = [
        f"Interview Summary: {candidate['name'] or 'Candidate'}",
        f"Candidate ID: {candidate['candidate_id'] or 'Not provided'}",
        f"Role: {candidate['role'] or 'Not provided'}",
        "",
        "STRENGTHS",
    ]

    if findings["strengths"]:
        lines.extend(f"- {item}" for item in findings["strengths"])
    else:
        lines.append("- No strengths were provided in the input.")

    lines.extend(["", "AREAS FOR DEVELOPMENT"])

    if findings["weaknesses"]:
        lines.extend(f"- {item}" for item in findings["weaknesses"])
    else:
        lines.append("- No development areas were provided in the input.")

    lines.extend(["", "JOB-RELATED COLLABORATION INDICATORS"])

    if summary["cultural_fit_indicators"]:
        lines.extend(
            f"- {item['indicator']}"
            for item in summary["cultural_fit_indicators"]
        )
    else:
        lines.append("- No collaboration indicators were provided.")

    lines.extend(["", "RISK FLAGS"])

    if summary["risk_flags"]:
        lines.extend(
            f"- {item['flag']} (requires human review)"
            for item in summary["risk_flags"]
        )
    else:
        lines.append("- No explicit risk flags were supplied.")

    lines.extend(["", "POSSIBLE INCONSISTENCIES"])

    if summary["inconsistencies"]:
        for item in summary["inconsistencies"]:
            lines.append(
                f"- Topic: {item['topic']}. "
                "Answers differ and should be checked in context."
            )
    else:
        lines.append("- No possible inconsistencies detected by the rules.")

    lines.extend([
        "",
        "OVERALL INTERVIEW PERFORMANCE",
        f"- Score: {performance['overall_score']}",
        f"- Summary: {performance['performance_label']}",
        "",
        "RECRUITER NOTE",
        "This report organizes the supplied interview evidence. "
        "Risk flags and inconsistencies require human review. "
        "Do not use this summary alone to make a hiring decision.",
    ])

    return "\n".join(lines)


def generate_interview_summary(interview):
    """Build the complete structured interview summary."""
    if not isinstance(interview, dict):
        raise ValueError("interview must be a dictionary.")

    candidate = {
        "candidate_id": clean_text(interview.get("candidate_id")),
        "name": clean_text(interview.get("candidate_name")),
        "role": clean_text(interview.get("role")),
    }

    scores = interview.get("scores", {})
    performance = calculate_overall_performance(scores)

    summary = {
        "candidate": candidate,
        "findings": build_strengths_and_weaknesses(interview),
        "cultural_fit_indicators": identify_cultural_fit_indicators(
            interview
        ),
        "risk_flags": identify_risk_flags(interview),
        "inconsistencies": identify_inconsistencies(
            interview.get("answers", [])
        ),
        "overall_performance": performance,
        "missing_data": [],
        "report_type": "HR_INTERVIEW_SUMMARY",
        "human_review_required": True,
        "limitations": [
            "The summary is based on supplied interview information.",
            "Possible inconsistencies are not proof of dishonesty.",
            "Collaboration indicators must be evaluated against job criteria.",
            "The report must not be the sole basis for a hiring decision.",
        ],
    }

    if not candidate["candidate_id"]:
        summary["missing_data"].append("candidate_id")

    if not candidate["role"]:
        summary["missing_data"].append("role")

    if not summary["findings"]["strengths"]:
        summary["missing_data"].append("strengths")

    if not summary["findings"]["weaknesses"]:
        summary["missing_data"].append("weaknesses")

    if performance["overall_score"] is None:
        summary["missing_data"].append("scores")

    summary["natural_language_report"] = (
        generate_natural_language_report(summary)
    )

    return summary


def save_interview_report(summary, output_dir):
    """Save a structured JSON report and a readable Markdown report."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    candidate_id = summary["candidate"]["candidate_id"] or "candidate"
    safe_id = re.sub(r"[^A-Za-z0-9_-]", "_", candidate_id)

    json_path = output_dir / f"{safe_id}_interview_summary.json"
    markdown_path = output_dir / f"{safe_id}_interview_summary.md"

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2, ensure_ascii=False)

    markdown = [
        "# AI Interview Summary",
        "",
        f"**Candidate:** {summary['candidate']['name'] or 'Not provided'}",
        f"**Candidate ID:** {summary['candidate']['candidate_id'] or 'Not provided'}",
        f"**Role:** {summary['candidate']['role'] or 'Not provided'}",
        "",
        "## Strengths",
    ]

    markdown.extend(
        f"- {item}" for item in summary["findings"]["strengths"]
    )

    if not summary["findings"]["strengths"]:
        markdown.append("- Not provided")

    markdown.extend(["", "## Weaknesses / Development Areas"])

    markdown.extend(
        f"- {item}" for item in summary["findings"]["weaknesses"]
    )

    if not summary["findings"]["weaknesses"]:
        markdown.append("- Not provided")

    markdown.extend(["", "## Collaboration Indicators"])

    markdown.extend(
        f"- {item['indicator']}"
        for item in summary["cultural_fit_indicators"]
    )

    if not summary["cultural_fit_indicators"]:
        markdown.append("- Not provided")

    markdown.extend(["", "## Risk Flags"])

    markdown.extend(
        f"- {item['flag']} (human review required)"
        for item in summary["risk_flags"]
    )

    if not summary["risk_flags"]:
        markdown.append("- No explicit risk flags supplied")

    markdown.extend(["", "## Possible Inconsistencies"])

    markdown.extend(
        f"- {item['topic']}: {item['first_answer']} / "
        f"{item['second_answer']}"
        for item in summary["inconsistencies"]
    )

    if not summary["inconsistencies"]:
        markdown.append("- None detected by the configured rules")

    markdown.extend([
        "",
        "## Overall Performance",
        f"- Score: {summary['overall_performance']['overall_score']}",
        f"- Label: {summary['overall_performance']['performance_label']}",
        "",
        "## Natural-Language Summary",
        "",
        summary["natural_language_report"],
        "",
        "## Review Notice",
        "This report organizes supplied evidence. Human review is required. "
        "It must not be the sole basis for a hiring decision.",
        "",
    ])

    markdown_path.write_text("\n".join(markdown), encoding="utf-8")

    return json_path, markdown_path
