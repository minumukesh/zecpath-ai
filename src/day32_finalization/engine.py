from pathlib import Path
from datetime import datetime, timezone
import json


PROJECT_ROOT = Path(__file__).resolve().parents[2]


EXPECTED_COMPONENTS = {
    "resume_extraction": "src/resume_extraction",
    "job_description_parser": "src/jd_parser",
    "ats_scoring_api": "src/ats_api",
    "ats_pipeline": "src/ats_pipeline",
    "answer_understanding": "src/answer_understanding",
    "screening_scoring": "src/screening_scoring",
    "screening_report": "src/screening_report",
    "conversation_flow": "src/conversation_flow",
    "screening_optimization": "src/screening_optimization",
    "edge_case_handling": "src/edge_case_handling",
}


def inspect_project(root: Path = PROJECT_ROOT) -> dict:
    """Inspect the repository without modifying existing components."""
    components = {}

    for name, relative_path in EXPECTED_COMPONENTS.items():
        path = root / relative_path
        components[name] = {
            "path": relative_path.replace("\\", "/"),
            "exists": path.exists(),
            "type": (
                "directory" if path.is_dir()
                else "file" if path.is_file()
                else "missing"
            ),
        }

    existing_count = sum(
        1 for component in components.values()
        if component["exists"]
    )

    return {
        "project": "Zecpath AI",
        "inspection_time_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(root),
        "components_checked": len(components),
        "components_found": existing_count,
        "components_missing": len(components) - existing_count,
        "components": components,
    }


def load_demo_cases(path: Path) -> list:
    """Load finalization demo cases from JSON."""
    with path.open("r", encoding="utf-8-sig") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Demo dataset must contain a JSON list.")

    for index, case in enumerate(data, start=1):
        if not isinstance(case, dict):
            raise ValueError(f"Demo case {index} must be a JSON object.")

        for field in ("candidate_id", "role", "resume_text", "job_description"):
            if not str(case.get(field, "")).strip():
                raise ValueError(
                    f"Demo case {index} is missing required field: {field}"
                )

    return data


def evaluate_demo_case(case: dict) -> dict:
    """
    Run a transparent finalization demonstration.

    This standalone fallback uses the supplied resume and job description.
    It does not claim to invoke the existing ATS pipeline automatically.
    """
    resume_text = case["resume_text"].strip()
    job_description = case["job_description"].strip()

    resume_lower = resume_text.lower()
    job_lower = job_description.lower()

    common_terms = [
        "python", "sql", "excel", "power bi", "tableau",
        "communication", "business analysis", "machine learning",
        "java", "javascript", "pandas", "numpy", "git",
    ]

    matched_skills = [
        term for term in common_terms
        if term in resume_lower and term in job_lower
    ]

    required_terms = [
        term for term in common_terms
        if term in job_lower
    ]

    skill_score = (
        len(matched_skills) / len(required_terms) * 100
        if required_terms else 0.0
    )

    # This demo provides a transparent keyword-overlap indicator only.
    # It is not a replacement for the project's established ATS score.
    decision = (
        "REVIEW"
        if skill_score < 50
        else "DEMO_MATCH"
    )

    return {
        "candidate_id": case["candidate_id"],
        "role": case["role"],
        "matched_terms": matched_skills,
        "job_terms_checked": required_terms,
        "demo_keyword_overlap_score": round(skill_score, 2),
        "demo_result": decision,
        "note": (
            "Demonstration-only keyword overlap. This is not the official "
            "ATS score or a hiring decision. Use the existing ATS pipeline "
            "for production evaluation."
        ),
    }


def build_finalization_report(root: Path, cases: list) -> dict:
    """Create project readiness and demo evaluation reports."""
    inspection = inspect_project(root)

    demo_results = [
        evaluate_demo_case(case)
        for case in cases
    ]

    return {
        "project": "Zecpath AI",
        "day": 32,
        "title": "Screening System Finalization",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_inspection": inspection,
        "demo": {
            "demo_type": "Standalone finalization demonstration",
            "cases_processed": len(demo_results),
            "results": demo_results,
            "important_note": (
                "The standalone demo demonstrates the report structure "
                "and basic keyword overlap. It does not automatically "
                "execute every existing ATS, voice, or screening module."
            ),
        },
        "finalization_checklist": {
            "system_documentation": "GENERATED",
            "api_design_explanation": "GENERATED",
            "end_to_end_demo": "GENERATED",
            "code_handover_checklist": "GENERATED",
            "project_component_inspection": "COMPLETED",
            "production_deployment": "NOT_VERIFIED",
            "live_api_execution": "NOT_VERIFIED",
        },
        "production_readiness_notes": [
            "Confirm all required components exist.",
            "Run the full project test suite.",
            "Verify API endpoints and request/response schemas.",
            "Run an end-to-end demonstration through the actual ATS pipeline.",
            "Review error handling, logging, and security settings.",
            "Do not claim live deployment without deployment evidence.",
            "Require human review for uncertain screening results.",
        ],
    }


def write_reports(root: Path, report: dict) -> dict:
    """Write JSON and Markdown reports."""
    output_dir = root / "outputs" / "day32"
    docs_dir = root / "docs" / "day32"

    output_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "day32_finalization_report.json"
    markdown_path = output_dir / "day32_finalization_report.md"

    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    inspection = report["project_inspection"]

    lines = [
        "# Day 32 - Screening System Finalization",
        "",
        "## Objective",
        "",
        "Prepare final system documentation, explain the API design,",
        "demonstrate the screening workflow, and prepare a code handover.",
        "",
        "## System Workflow",
        "",
        "Candidate Resume + Job Description",
        "→ Resume Extraction and Job Description Parsing",
        "→ Candidate Analysis",
        "→ ATS Scoring",
        "→ Candidate Ranking and Eligibility",
        "→ Screening Report",
        "→ Recruiter Review",
        "",
        "The diagram describes the intended workflow. Confirm each connection",
        "against the existing implementation before presenting it as live integration.",
        "",
        "## API Design",
        "",
        "1. The client submits a resume or requests screening.",
        "2. The API validates the request and required files.",
        "3. The backend invokes the configured screening pipeline.",
        "4. The service returns a result or asynchronous job status.",
        "5. Errors should use consistent responses and be recorded in logs.",
        "",
        "Use the existing API routes and schemas as the source of truth.",
        "This document does not invent new production endpoints.",
        "",
        "## Project Component Inspection",
        "",
        f"- Components checked: {inspection['components_checked']}",
        f"- Components found: {inspection['components_found']}",
        f"- Components missing: {inspection['components_missing']}",
        "",
        "| Component | Expected path | Status |",
        "|---|---|---|",
    ]

    for name, component in inspection["components"].items():
        status = "FOUND" if component["exists"] else "NOT FOUND"
        lines.append(
            f"| {name} | `{component['path']}` | {status} |"
        )

    lines.extend([
        "",
        "## Demonstration Results",
        "",
        f"- Demo cases processed: {report['demo']['cases_processed']}",
        "",
        "| Candidate | Role | Demo overlap score | Demo result |",
        "|---|---|---:|---|",
    ])

    for result in report["demo"]["results"]:
        lines.append(
            f"| {result['candidate_id']} "
            f"| {result['role']} "
            f"| {result['demo_keyword_overlap_score']:.2f} "
            f"| {result['demo_result']} |"
        )

    lines.extend([
        "",
        "**Important:** The demonstration score is a simple keyword-overlap",
        "indicator. It is not the official ATS score or a hiring decision.",
        "",
        "## Handover Checklist",
        "",
        "- [ ] Confirm all source files are included.",
        "- [ ] Confirm dependencies and virtual environment instructions.",
        "- [ ] Run the full automated test suite.",
        "- [ ] Verify API routes and schemas.",
        "- [ ] Review configuration and environment variables.",
        "- [ ] Review logging and error-handling behavior.",
        "- [ ] Save real screenshots of the demo and passing tests.",
        "- [ ] Record known limitations and future improvements.",
        "- [ ] Confirm deployment separately if required.",
        "",
        "## Production Readiness",
        "",
        "Generating this report does not itself make the system production-ready.",
        "Actual API integration, security, deployment, and end-to-end behavior",
        "must be verified separately.",
        "",
        "## Generated Files",
        "",
        "- `outputs/day32/day32_finalization_report.json`",
        "- `outputs/day32/day32_finalization_report.md`",
        "- `docs/day32/day32_technical_handover.md`",
        "",
    ])

    markdown_path.write_text("\n".join(lines), encoding="utf-8")

    handover_path = docs_dir / "day32_technical_handover.md"

    handover_content = """# Zecpath AI - Technical Handover

## Project purpose
The screening system processes candidate information and supports recruiters
with structured evaluation results.

## High-level workflow
Candidate Resume + Job Description
→ Resume Extraction and JD Parsing
→ Candidate Analysis
→ ATS Scoring
→ Candidate Ranking and Eligibility
→ Screening Report
→ Recruiter Review

Verify the actual code paths before describing every stage as integrated.

## API design
- Validate incoming requests.
- Validate uploaded file types and required parameters.
- Pass valid requests to the existing backend and ATS pipeline.
- Return structured results or job status.
- Handle failures with consistent error responses.
- Log errors without exposing private candidate information.

Use the project's existing API routes and schemas. Do not assume an endpoint
exists unless it is present in the source code.

## Run instructions
1. Open the project root in a terminal.
2. Activate the project's virtual environment.
3. Install dependencies from the project's existing dependency file.
4. Run the demo and automated tests.
5. Review the generated JSON and Markdown reports.

## Handover checklist
- [ ] Source code reviewed
- [ ] Dependencies documented
- [ ] API routes verified
- [ ] Automated tests passed
- [ ] Error handling reviewed
- [ ] Configuration documented
- [ ] Real demo screenshots saved
- [ ] Known limitations recorded
- [ ] Deployment verified separately, if applicable

## Limitations
A successful local demo or test suite does not prove production deployment.
The standalone Day 32 demo uses a keyword-overlap indicator and is not the
official ATS scoring engine. Human review remains necessary for uncertain cases.
"""

    handover_path.write_text(handover_content, encoding="utf-8")

    return {
        "json_report": json_path,
        "markdown_report": markdown_path,
        "handover_document": handover_path,
    }
