import json
import shutil
from pathlib import Path

from src.day55_governance.engine import GovernanceEngine, GovernanceError


def main():

    demo_root = Path("outputs/day55/demo_secure_storage")

    if demo_root.exists():
        shutil.rmtree(demo_root)

    engine = GovernanceEngine(demo_root)

    print("\n============================================")
    print(" DAY 55 - SECURITY & AI GOVERNANCE")
    print("============================================")

    # 1. Consent
    print("\n1. CONSENT MANAGEMENT")

    engine.record_consent(
        "CAND001",
        "HR_INTERVIEW",
        True,
        actor="admin"
    )

    print("Candidate consent recorded.")
    print(
        "Consent valid:",
        engine.has_consent("CAND001", "HR_INTERVIEW")
    )

    # 2. Score and decision audit logs
    print("\n2. AUDIT TRAIL")

    engine.log_score(
        "hr_manager",
        "CAND001",
        86,
        "HR_Scoring_Model_v1",
        role="admin"
    )

    engine.log_decision(
        "hr_manager",
        "CAND001",
        "RECOMMEND",
        "Interview evidence reviewed by HR manager.",
        role="admin"
    )

    print(
        "Audit verification:",
        engine.verify_audit_trail("admin")
    )

    # 3. Transcript storage
    print("\n3. TRANSCRIPT STORAGE")

    engine.store_data(
        role="interviewer",
        category="transcripts",
        record_id="TR001",
        candidate_id="CAND001",
        content={
            "interview_stage": "HR",
            "transcript": "Demonstration transcript.",
            "review_status": "pending"
        },
        purpose="HR_INTERVIEW",
        actor="interviewer"
    )

    print("Transcript stored with consent.")

    # 4. Report storage
    print("\n4. REPORT STORAGE")

    engine.store_data(
        role="hr_manager",
        category="reports",
        record_id="RP001",
        candidate_id="CAND001",
        content={
            "score": 86,
            "recommendation": "RECOMMEND",
            "human_review": True
        },
        purpose="HR_INTERVIEW",
        actor="hr_manager"
    )

    print("Report stored with consent.")

    # 5. Access control
    print("\n5. ROLE-BASED ACCESS CONTROL")

    try:
        engine.read_data(
            "interviewer",
            "reports",
            "RP001",
            "interviewer"
        )

    except GovernanceError as error:
        print("Unauthorized report access blocked:", error)

    report = engine.read_data(
        "hr_manager",
        "reports",
        "RP001",
        "hr_manager"
    )

    print("Authorized report access:", report["record_id"])

    # 6. Retention
    print("\n6. DATA RETENTION")

    retention = engine.apply_retention("admin")

    print("Retention execution:", retention["status"])

    # 7. Final verification
    print("\n7. GOVERNANCE SUMMARY")

    summary = engine.governance_summary()

    print(json.dumps(summary, indent=4))

    # Save output
    output = Path("outputs/day55/governance_demo_results.json")

    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(
        json.dumps(
            {
                "governance_summary": summary,
                "audit_integrity": engine.verify_audit_trail("admin"),
                "retention_result": retention
            },
            indent=4
        ),
        encoding="utf-8"
    )

    print("\nDemo result saved:", output)

    print("\n============================================")
    print(" DAY 55 DEMONSTRATION COMPLETED")
    print("============================================")


if __name__ == "__main__":
    main()
