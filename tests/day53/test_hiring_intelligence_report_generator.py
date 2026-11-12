import unittest

from src.interview_system.hiring_intelligence_report_generator import (
    HiringIntelligenceReportGenerator
)


class TestHiringIntelligenceReportGenerator(unittest.TestCase):

    def setUp(self):

        self.generator = HiringIntelligenceReportGenerator()

    def make_candidate(self, **changes):

        data = {

            "candidate": {
                "candidate_id": "TEST-053",
                "candidate_name": "Test Candidate",
                "target_role": "Data Analyst",
                "experience": "Fresher",
                "skills": ["Python", "SQL"]
            },

            "ats": {
                "score": 85,
                "summary": "Good ATS match."
            },

            "screening": {
                "score": 80,
                "summary": "Screening passed."
            },

            "hr_interview": {
                "score": 82,
                "summary": "Good HR interview."
            },

            "technical_interview": {
                "score": 90,
                "machine_test_score": 88,
                "summary": "Strong technical performance."
            },

            "behavioral": {
                "task_focus_score": 80,
                "observations": []
            },

            "integrity": {
                "flags": []
            },

            "final_decision": {
                "recommendation": "SELECTED",
                "hiring_fit_score": 85,
                "confidence_score": 90,
                "explanation": "Strong overall performance."
            },

            "strengths": ["Good analytical skills."],

            "weaknesses": ["Limited industry experience."],

            "evidence_verified": True,

            "missing_stages": []
        }

        data.update(changes)

        return data

    def test_report_generation(self):

        report = self.generator.generate_report(
            self.make_candidate()
        )

        self.assertEqual(report["day"], 53)

    def test_candidate_profile(self):

        report = self.generator.generate_report(
            self.make_candidate()
        )

        self.assertEqual(
            report["candidate_profile"]["candidate_name"],
            "Test Candidate"
        )

    def test_ats_summary(self):

        report = self.generator.generate_report(
            self.make_candidate()
        )

        self.assertEqual(
            report["evaluation_summary"]["ats"]["score"],
            85
        )

    def test_screening_summary(self):

        report = self.generator.generate_report(
            self.make_candidate()
        )

        self.assertEqual(
            report["evaluation_summary"]["screening"]["score"],
            80
        )

    def test_hr_summary(self):

        report = self.generator.generate_report(
            self.make_candidate()
        )

        self.assertEqual(
            report["evaluation_summary"]["hr_interview"]["score"],
            82
        )

    def test_technical_summary(self):

        report = self.generator.generate_report(
            self.make_candidate()
        )

        self.assertEqual(
            report["evaluation_summary"]["technical_interview"]["score"],
            90
        )

    def test_machine_test_summary(self):

        report = self.generator.generate_report(
            self.make_candidate()
        )

        self.assertEqual(
            report["evaluation_summary"]["technical_interview"]["machine_test_score"],
            88
        )

    def test_strengths_generated(self):

        report = self.generator.generate_report(
            self.make_candidate()
        )

        self.assertGreater(
            len(report["candidate_assessment"]["strengths"]),
            0
        )

    def test_weaknesses_generated(self):

        report = self.generator.generate_report(
            self.make_candidate()
        )

        self.assertGreater(
            len(report["candidate_assessment"]["weaknesses"]),
            0
        )

    def test_integrity_flags_recorded(self):

        report = self.generator.generate_report(
            self.make_candidate(
                integrity={
                    "flags": [
                        {
                            "description": "Repeated tab switching."
                        }
                    ]
                }
            )
        )

        self.assertEqual(
            report["integrity_analysis"]["flag_count"],
            1
        )

    def test_integrity_flag_is_not_proof(self):

        report = self.generator.generate_report(
            self.make_candidate(
                integrity={
                    "flags": ["External voice event"]
                }
            )
        )

        interpretation = (
            report["integrity_analysis"]["flags"][0]["interpretation"]
        )

        self.assertIn("not proof", interpretation)

    def test_missing_stage_recorded(self):

        report = self.generator.generate_report(
            self.make_candidate(
                missing_stages=["machine_test"]
            )
        )

        self.assertEqual(
            len(report["candidate_assessment"]["risk_indicators"]),
            1
        )

    def test_unverified_evidence_recorded(self):

        report = self.generator.generate_report(
            self.make_candidate(evidence_verified=False)
        )

        self.assertTrue(
            any(
                item["category"] == "EVIDENCE"
                for item in report["candidate_assessment"]["risk_indicators"]
            )
        )

    def test_behavioral_context_is_explained(self):

        report = self.generator.generate_report(
            self.make_candidate()
        )

        self.assertIn(
            "not measures of honesty",
            report["behavioral_analysis"]["interpretation"]
        )

    def test_final_recommendation(self):

        report = self.generator.generate_report(
            self.make_candidate()
        )

        self.assertEqual(
            report["final_recommendation"]["recommendation"],
            "SELECTED"
        )

    def test_missing_candidate_profile_fails(self):

        with self.assertRaises(ValueError):

            self.generator.generate_report({})

    def test_invalid_score_fails(self):

        with self.assertRaises(ValueError):

            self.generator.generate_report(
                self.make_candidate(
                    ats={"score": 150}
                )
            )

    def test_report_disclaimer_exists(self):

        report = self.generator.generate_report(
            self.make_candidate()
        )

        self.assertIn(
            "human review",
            report["report_disclaimer"]
        )


if __name__ == "__main__":
    unittest.main()
