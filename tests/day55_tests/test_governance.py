import tempfile
import unittest

from pathlib import Path

from src.day55_governance.engine import (
    GovernanceEngine,
    GovernanceError
)


class Day55GovernanceTests(unittest.TestCase):

    def setUp(self):

        self.temp = tempfile.TemporaryDirectory()

        self.engine = GovernanceEngine(
            Path(self.temp.name) / "secure_storage"
        )

        self.engine.record_consent(
            "C001",
            "INTERVIEW",
            True
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_consent_granted(self):

        self.assertTrue(
            self.engine.has_consent("C001", "INTERVIEW")
        )

    def test_consent_denied(self):

        self.engine.record_consent(
            "C002",
            "INTERVIEW",
            False
        )

        self.assertFalse(
            self.engine.has_consent("C002", "INTERVIEW")
        )

    def test_latest_consent_controls_status(self):

        self.engine.record_consent(
            "C001",
            "INTERVIEW",
            False
        )

        self.assertFalse(
            self.engine.has_consent("C001", "INTERVIEW")
        )

    def test_storage_requires_consent(self):

        with self.assertRaises(GovernanceError):

            self.engine.store_data(
                "interviewer",
                "transcripts",
                "T001",
                "UNKNOWN",
                {"text": "Test"},
                "INTERVIEW",
                "interviewer"
            )

    def test_transcript_storage(self):

        result = self.engine.store_data(
            "interviewer",
            "transcripts",
            "T001",
            "C001",
            {"text": "Test transcript"},
            "INTERVIEW",
            "interviewer"
        )

        self.assertEqual(result["status"], "stored")

    def test_report_storage(self):

        result = self.engine.store_data(
            "hr_manager",
            "reports",
            "R001",
            "C001",
            {"score": 80},
            "INTERVIEW",
            "hr_manager"
        )

        self.assertEqual(result["status"], "stored")

    def test_access_control_blocks_unauthorized_role(self):

        with self.assertRaises(GovernanceError):

            self.engine.read_data(
                "interviewer",
                "reports",
                "R001",
                "interviewer"
            )

    def test_admin_can_read_audit(self):

        result = self.engine.verify_audit_trail("admin")

        self.assertTrue(result["valid"])

    def test_auditor_can_verify_audit(self):

        result = self.engine.verify_audit_trail("auditor")

        self.assertTrue(result["valid"])

    def test_interviewer_cannot_verify_audit(self):

        with self.assertRaises(GovernanceError):

            self.engine.verify_audit_trail("interviewer")

    def test_score_logging(self):

        result = self.engine.log_score(
            "admin",
            "C001",
            85,
            "TestModel"
        )

        self.assertEqual(
            result["event_type"],
            "SCORE_GENERATED"
        )

    def test_invalid_score_rejected(self):

        with self.assertRaises(GovernanceError):

            self.engine.log_score(
                "admin",
                "C001",
                120,
                "TestModel"
            )

    def test_decision_logging(self):

        result = self.engine.log_decision(
            "admin",
            "C001",
            "RECOMMEND",
            "Evidence reviewed."
        )

        self.assertEqual(
            result["event_type"],
            "HIRING_DECISION"
        )

    def test_audit_tampering_detection(self):

        self.engine.log_event(
            "admin",
            "TEST_EVENT",
            "test",
            "R001"
        )

        records = self.engine._read_audit_records()

        records[0]["actor"] = "modified_actor"

        with self.engine.audit_file.open(
            "w",
            encoding="utf-8"
        ) as file:

            for record in records:
                import json
                file.write(json.dumps(record) + "\n")

        result = self.engine.verify_audit_trail("admin")

        self.assertFalse(result["valid"])

    def test_data_deletion(self):

        self.engine.store_data(
            "interviewer",
            "transcripts",
            "T002",
            "C001",
            {"text": "Delete me"},
            "INTERVIEW",
            "interviewer"
        )

        result = self.engine.delete_data(
            "admin",
            "transcripts",
            "T002",
            "admin"
        )

        self.assertEqual(result["status"], "deleted")

    def test_invalid_category_rejected(self):

        with self.assertRaises(GovernanceError):

            self.engine.store_data(
                "admin",
                "unknown",
                "X001",
                "C001",
                {},
                "INTERVIEW",
                "admin"
            )

    def test_governance_summary(self):

        summary = self.engine.governance_summary()

        self.assertTrue(summary["consent_required"])

        self.assertIn(
            "admin",
            summary["access_roles"]
        )


if __name__ == "__main__":
    unittest.main()
