import unittest
from datetime import datetime, timezone, timedelta

from src.hr_ai_ethics.engine import (
    validate_consent,
    remove_demographic_signals,
    generate_explainability_notes,
    audit_group_fairness,
    check_data_retention,
    generate_compliance_report
)


class TestDay43(unittest.TestCase):

    def consent_record(self):
        return {
            "consent_given": True,
            "purpose": "Recruitment evaluation",
            "consent_timestamp": datetime.now(timezone.utc).isoformat(),
            "policy_version": "1.0",
            "withdrawn": False
        }

    def test_valid_consent(self):
        self.assertTrue(validate_consent(self.consent_record())["valid"])

    def test_consent_not_granted(self):
        record = self.consent_record()
        record["consent_given"] = False
        self.assertFalse(validate_consent(record)["valid"])

    def test_withdrawn_consent(self):
        record = self.consent_record()
        record["withdrawn"] = True
        self.assertEqual(
            validate_consent(record)["status"],
            "CONSENT_WITHDRAWN"
        )

    def test_missing_consent_fields(self):
        self.assertFalse(validate_consent({})["valid"])

    def test_demographic_removal(self):
        result = remove_demographic_signals({
            "candidate_id": "C001",
            "gender": "Sample",
            "age": 25,
            "skills": ["Python"]
        })
        self.assertNotIn("gender", result["cleaned_data"])
        self.assertNotIn("age", result["cleaned_data"])
        self.assertIn("skills", result["cleaned_data"])

    def test_nested_demographic_removal(self):
        result = remove_demographic_signals({
            "candidate": {
                "name": "Sample",
                "caste": "Sample"
            }
        })
        self.assertNotIn(
            "caste", result["cleaned_data"]["candidate"]
        )

    def test_explainability(self):
        result = generate_explainability_notes(
            {"communication": 80},
            {"communication": 25},
            80
        )
        self.assertEqual(result["final_score"], 80)
        self.assertTrue(result["component_notes"])

    def test_fairness_review(self):
        outcomes = (
            [{"audit_group": "A", "selected": True}] * 4
            + [{"audit_group": "A", "selected": False}] * 2
            + [{"audit_group": "B", "selected": True}] * 3
            + [{"audit_group": "B", "selected": False}] * 3
        )
        result = audit_group_fairness(outcomes)
        self.assertEqual(result["status"], "REVIEW_REQUIRED")

    def test_small_group_suppression(self):
        result = audit_group_fairness([
            {"audit_group": "A", "selected": True},
            {"audit_group": "B", "selected": False}
        ])
        self.assertEqual(
            result["status"], "INSUFFICIENT_GROUP_DATA"
        )

    def test_active_retention(self):
        now = datetime.now(timezone.utc)
        result = check_data_retention(
            (now - timedelta(days=30)).isoformat(),
            365,
            now
        )
        self.assertEqual(
            result["status"], "WITHIN_RETENTION_PERIOD"
        )

    def test_expired_retention(self):
        now = datetime.now(timezone.utc)
        result = check_data_retention(
            (now - timedelta(days=400)).isoformat(),
            365,
            now
        )
        self.assertTrue(result["expired"])

    def test_withdrawn_consent_retention_review(self):
        now = datetime.now(timezone.utc)
        result = check_data_retention(
            now.isoformat(), 365, now, True
        )
        self.assertEqual(
            result["status"], "REVIEW_FOR_EARLY_DELETION"
        )

    def test_compliance_report(self):
        consent = validate_consent(self.consent_record())
        fairness = audit_group_fairness(
            [{"audit_group": "A", "selected": True}] * 5
        )
        now = datetime.now(timezone.utc)
        retention = check_data_retention(
            now.isoformat(), 365, now
        )
        result = generate_compliance_report(
            consent, fairness, retention
        )
        self.assertEqual(result["total_checks"], 3)


if __name__ == "__main__":
    unittest.main()
