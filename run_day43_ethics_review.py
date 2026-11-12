import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

from src.hr_ai_ethics.engine import (
    validate_consent,
    remove_demographic_signals,
    generate_explainability_notes,
    audit_group_fairness,
    check_data_retention,
    generate_compliance_report
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs/day43"
DOCS = ROOT / "docs/day43"

OUT.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)


def main():
    now = datetime.now(timezone.utc)

    consent = validate_consent({
        "consent_given": True,
        "purpose": "AI-assisted recruitment interview evaluation",
        "consent_timestamp": now.isoformat(),
        "policy_version": "1.0",
        "withdrawn": False
    })

    candidate = {
        "candidate_id": "ETH-001",
        "skills": ["Python", "SQL", "Excel"],
        "experience_years": 2,
        "age": 25,
        "gender": "Sample",
        "religion": "Sample",
        "interview": {
            "communication_score": 85,
            "caste": "Sample"
        }
    }

    demographic = remove_demographic_signals(candidate)

    explainability = generate_explainability_notes(
        {
            "answer_relevance": 85,
            "communication": 80,
            "confidence": 75,
            "consistency": 90
        },
        {
            "answer_relevance": 40,
            "communication": 25,
            "confidence": 20,
            "consistency": 15
        },
        83
    )

    # Group-level audit data is separate from candidate scoring.
    group_outcomes = (
        [{"audit_group": "GROUP_A", "selected": True}] * 4
        + [{"audit_group": "GROUP_A", "selected": False}] * 2
        + [{"audit_group": "GROUP_B", "selected": True}] * 3
        + [{"audit_group": "GROUP_B", "selected": False}] * 3
    )

    fairness = audit_group_fairness(group_outcomes)

    retention = check_data_retention(
        (now - timedelta(days=30)).isoformat(),
        365,
        now
    )

    expired = check_data_retention(
        (now - timedelta(days=400)).isoformat(),
        365,
        now
    )

    compliance = generate_compliance_report(
        consent, fairness, retention
    )

    report = {
        "day": 43,
        "module": "Ethics and Compliance Review",
        "consent_review": consent,
        "demographic_signal_removal": demographic,
        "explainability": explainability,
        "fairness_review": fairness,
        "retention_review": {
            "active_record": retention,
            "expired_record": expired
        },
        "compliance_readiness": compliance
    }

    (OUT / "day43_ethics_compliance_report.json").write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    ethics = """# Day 43 - AI Ethics Documentation

## Consent Requirements
Record whether consent was granted, the purpose of processing,
the consent timestamp, and the policy version.
A withdrawn consent record requires review.

## Fairness of Scoring
Scoring should use job-related evidence and consistent criteria.
Demographic attributes must not be used as scoring inputs.

## Demographic Signal Removal
Configured demographic fields are removed before candidate data
is passed to the scoring workflow.

## Explainability
Component scores, configured weights, and the final score are
recorded to make the calculation reviewable.

## Data Retention
The system checks whether records remain within a configurable
retention period or require deletion review.

## Human Oversight
Recruiters should review ambiguous results and potential disparities.

This document describes technical controls. It is not legal advice.
"""

    fairness_notes = """# Day 43 - Fairness Review Notes

The fairness audit compares group-level selection rates using
separate audit data.

A selection-rate difference is a signal for further investigation,
not proof of discrimination.

Small groups are marked as insufficient sample.

Demographic group information is not passed into candidate scoring.
"""

    readiness = """# Day 43 - Compliance Readiness Report

The report checks:
1. Consent record completeness and validity.
2. Fairness review availability.
3. Data-retention status.

The demonstration uses a configurable 365-day retention period.
This is a project setting, not a statutory retention requirement.

Legal and organizational review is required before production use.
This report is not legal certification.
"""

    (DOCS / "AI_ETHICS_DOCUMENTATION.md").write_text(
        ethics, encoding="utf-8"
    )

    (DOCS / "FAIRNESS_REVIEW_NOTES.md").write_text(
        fairness_notes, encoding="utf-8"
    )

    (DOCS / "COMPLIANCE_READINESS_REPORT.md").write_text(
        readiness, encoding="utf-8"
    )

    print("=" * 60)
    print("DAY 43 - ETHICS AND COMPLIANCE REVIEW")
    print("=" * 60)
    print("Consent:", consent["status"])
    print("Demographic fields removed:", demographic["removed_count"])
    print("Fairness review:", fairness["status"])
    print("Retention:", retention["status"])
    print("Expired record:", expired["status"])
    print("Explainability notes: GENERATED")
    print("Compliance:", compliance["readiness_status"])
    print("JSON report generated.")
    print("Three documentation files generated.")
    print("DAY 43 DEMO COMPLETED")


if __name__ == "__main__":
    main()
