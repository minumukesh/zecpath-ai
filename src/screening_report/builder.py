import json
import re
from pathlib import Path
from datetime import datetime, timezone


DEFAULT_OUTPUT_DIRECTORY = Path("outputs/day28")


def _clean_text(value):
    """Convert a value to safe, readable text."""
    if value is None:
        return ""

    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)

    return str(value).strip()


def _normalise_skills(skills):
    """Convert skill input into a clean list of unique skills."""
    if skills is None:
        return []

    if isinstance(skills, str):
        skills = re.split(r"[,;\n]", skills)

    if not isinstance(skills, list):
        return []

    result = []
    seen = set()

    for skill in skills:
        if isinstance(skill, dict):
            skill = skill.get("name", skill.get("skill", ""))

        skill = _clean_text(skill)

        if not skill:
            continue

        key = skill.casefold()

        if key not in seen:
            result.append(skill)
            seen.add(key)

    return result


def _normalise_answers(answers):
    """Convert candidate answers into a consistent list."""
    if answers is None:
        return []

    if isinstance(answers, dict):
        answers = [
            {"question": question, "answer": answer}
            for question, answer in answers.items()
        ]

    if not isinstance(answers, list):
        return []

    normalised = []

    for item in answers:
        if isinstance(item, str):
            normalised.append({
                "question": "",
                "answer": item,
                "status": "provided",
            })
            continue

        if not isinstance(item, dict):
            continue

        question = _clean_text(
            item.get("question", item.get("question_text", ""))
        )

        answer = _clean_text(
            item.get("answer", item.get("response", ""))
        )

        status = _clean_text(item.get("status", "")).casefold()

        if not answer:
            status = "missing"
        elif status not in {"missing", "partial", "vague", "provided"}:
            status = "provided"

        normalised.append({
            "question": question,
            "answer": answer,
            "status": status,
        })

    return normalised


def _normalise_score(value):
    """Return a valid score from 0 to 100, or None."""
    if value is None or value == "":
        return None

    try:
        score = float(value)
    except (TypeError, ValueError):
        return None

    if not 0 <= score <= 100:
        return None

    return round(score, 2)


def _collect_missing_data(candidate, answers, skills):
    """Identify important report fields that are unavailable."""
    missing = []

    required_fields = {
        "candidate_id": candidate.get("candidate_id"),
        "job_role": candidate.get("job_role"),
        "ats_score": candidate.get("ats_score"),
    }

    for field, value in required_fields.items():
        if value is None or _clean_text(value) == "":
            missing.append(field)

    if not answers:
        missing.append("screening_answers")
    elif any(not item["answer"] for item in answers):
        missing.append("one_or_more_answers")

    if not skills:
        missing.append("confirmed_skills")

    if not _clean_text(candidate.get("salary_expectation")):
        missing.append("salary_expectation")

    if not _clean_text(candidate.get("availability")):
        missing.append("availability")

    return missing


def _collect_strengths(candidate, answers, skills, score):
    """Build strengths only from information actually supplied."""
    strengths = []

    if skills:
        strengths.append(
            "Skills recorded: " + ", ".join(skills)
        )

    answered_count = sum(
        1 for item in answers
        if item["answer"] and item["status"] == "provided"
    )

    if answered_count:
        strengths.append(
            f"{answered_count} screening answer(s) were provided."
        )

    if score is not None and score >= 70:
        strengths.append(
            "The recorded ATS score meets or exceeds 70."
        )

    supplied_strengths = candidate.get("strengths", [])

    if isinstance(supplied_strengths, str):
        supplied_strengths = [supplied_strengths]

    if isinstance(supplied_strengths, list):
        for strength in supplied_strengths:
            strength = _clean_text(strength)

            if strength and strength not in strengths:
                strengths.append(strength)

    if not strengths:
        strengths.append(
            "No verified strengths could be derived from the supplied data."
        )

    return strengths


def _collect_risks(candidate, answers, missing, score):
    """Collect review points without inventing candidate problems."""
    risks = []

    for item in answers:
        if item["status"] == "missing":
            risks.append(
                f"Missing answer: {item['question'] or 'Unlabelled question'}"
            )
        elif item["status"] in {"partial", "vague"}:
            risks.append(
                f"{item['status'].capitalize()} answer: "
                f"{item['question'] or 'Unlabelled question'}"
            )

    if score is not None and score < 50:
        risks.append(
            "The recorded ATS score is below 50 and may need review."
        )

    if candidate.get("risk_notes"):
        notes = candidate["risk_notes"]

        if isinstance(notes, str):
            notes = [notes]

        if isinstance(notes, list):
            risks.extend(
                _clean_text(note)
                for note in notes
                if _clean_text(note)
            )

    if missing:
        risks.append(
            "Some report information is missing. Review the missing-data list."
        )

    if not risks:
        risks.append(
            "No specific risks were identified from the supplied data. "
            "This does not guarantee that no risks exist."
        )

    return risks


def build_screening_report(candidate):
    """
    Build a recruiter-friendly screening report.

    The generator summarises supplied data. It does not independently
    verify skills, predict performance, or make a hiring decision.
    """
    if not isinstance(candidate, dict):
        raise TypeError("Candidate input must be a dictionary.")

    candidate_id = _clean_text(candidate.get("candidate_id")) or "UNKNOWN"
    name = _clean_text(candidate.get("candidate_name")) or "Not provided"
    role = _clean_text(candidate.get("job_role")) or "Not provided"

    score = _normalise_score(candidate.get("ats_score"))

    answers = _normalise_answers(
        candidate.get("answers", candidate.get("screening_answers", []))
    )

    skills = _normalise_skills(
        candidate.get("confirmed_skills", candidate.get("skills", []))
    )

    missing_data = _collect_missing_data(candidate, answers, skills)

    strengths = _collect_strengths(
        candidate, answers, skills, score
    )

    risks = _collect_risks(
        candidate, answers, missing_data, score
    )

    key_answers = [
        {
            "question": item["question"] or "Question not specified",
            "answer": item["answer"] or "No answer provided",
            "status": item["status"],
        }
        for item in answers
    ]

    if score is None:
        score_status = "Not available"
    elif score >= 70:
        score_status = "Recorded score is 70 or above"
    elif score >= 50:
        score_status = "Recorded score is between 50 and 69.99"
    else:
        score_status = "Recorded score is below 50"

    report = {
        "report_metadata": {
            "report_type": "AI Screening Report",
            "report_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "candidate": {
            "candidate_id": candidate_id,
            "candidate_name": name,
            "job_role": role,
        },
        "screening_summary": {
            "ats_score": score,
            "score_status": score_status,
            "key_answers": key_answers,
            "strengths": strengths,
            "risks": risks,
            "missing_data": missing_data,
        },
        "screening_highlights": {
            "salary_expectation": (
                _clean_text(candidate.get("salary_expectation"))
                or "Not provided"
            ),
            "availability": (
                _clean_text(candidate.get("availability"))
                or "Not provided"
            ),
            "confirmed_skills": skills,
        },
        "recruiter_review": {
            "recommendation": (
                "Review the report alongside the original application "
                "and interview evidence."
            ),
            "automated_hiring_decision": None,
        },
        "limitations": [
            "The report reflects only the supplied information.",
            "Listed skills are not independently verified by this report generator.",
            "Missing information is not automatically proof of a candidate weakness.",
            "The report does not make a final hiring decision.",
        ],
    }

    return report


def generate_markdown_report(report):
    """Convert a screening report to a recruiter-friendly Markdown file."""
    candidate = report["candidate"]
    summary = report["screening_summary"]
    highlights = report["screening_highlights"]
    review = report["recruiter_review"]

    lines = [
        "# AI Screening Report",
        "",
        "## Candidate Details",
        f"- **Candidate ID:** {candidate['candidate_id']}",
        f"- **Candidate Name:** {candidate['candidate_name']}",
        f"- **Job Role:** {candidate['job_role']}",
        "",
        "## Screening Summary",
        f"- **ATS Score:** {summary['ats_score'] if summary['ats_score'] is not None else 'Not available'}",
        f"- **Score Status:** {summary['score_status']}",
        "",
        "## Key Answers",
    ]

    if summary["key_answers"]:
        for item in summary["key_answers"]:
            lines.extend([
                f"- **Question:** {item['question']}",
                f"  - **Answer:** {item['answer']}",
                f"  - **Status:** {item['status']}",
            ])
    else:
        lines.append("- No screening answers were supplied.")

    lines.extend(["", "## Strengths"])

    for item in summary["strengths"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Risks and Review Points"])

    for item in summary["risks"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Missing Data"])

    if summary["missing_data"]:
        for item in summary["missing_data"]:
            lines.append(f"- {item}")
    else:
        lines.append("- No missing fields were identified by the configured checks.")

    lines.extend([
        "",
        "## Screening Highlights",
        f"- **Salary Expectation:** {highlights['salary_expectation']}",
        f"- **Availability:** {highlights['availability']}",
        f"- **Confirmed Skills:** {', '.join(highlights['confirmed_skills']) or 'Not provided'}",
        "",
        "## Recruiter Review",
        review["recommendation"],
        "",
        "No automated final hiring decision was made.",
        "",
        "## Limitations",
    ])

    for item in report["limitations"]:
        lines.append(f"- {item}")

    lines.extend([
        "",
        f"_Report generated at: {report['report_metadata']['generated_at']}_",
        "",
    ])

    return "\n".join(lines)


def save_screening_report(candidate, output_directory=DEFAULT_OUTPUT_DIRECTORY):
    """Save a candidate report as JSON and Markdown."""
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)

    report = build_screening_report(candidate)

    safe_id = re.sub(
        r"[^A-Za-z0-9_-]+",
        "_",
        report["candidate"]["candidate_id"]
    ).strip("_") or "UNKNOWN"

    json_path = output_directory / f"{safe_id}_screening_report.json"
    markdown_path = output_directory / f"{safe_id}_screening_report.md"

    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    markdown_path.write_text(
        generate_markdown_report(report),
        encoding="utf-8",
    )

    return {
        "report": report,
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }


def generate_sample_reports(candidates, output_directory=DEFAULT_OUTPUT_DIRECTORY):
    """Generate reports for multiple sample candidates."""
    if not isinstance(candidates, list):
        raise TypeError("Candidates must be supplied as a list.")

    results = []

    for candidate in candidates:
        results.append(
            save_screening_report(candidate, output_directory)
        )

    summary_path = Path(output_directory) / "day28_report_generation_summary.json"

    summary = {
        "total_candidates": len(results),
        "reports_generated": len(results),
        "report_files": [
            {
                "candidate_id": result["report"]["candidate"]["candidate_id"],
                "json_path": result["json_path"],
                "markdown_path": result["markdown_path"],
            }
            for result in results
        ],
    }

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return {
        "results": results,
        "summary": summary,
        "summary_path": str(summary_path),
    }
