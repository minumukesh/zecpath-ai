import json
import tempfile
import unittest

from src.hr_interview_scoring import (
    DEFAULT_WEIGHTS,
    validate_weights,
    validate_score,
    normalize_interview_scores,
    classify_interview_score,
    score_hr_interview,
    save_interview_report,
)


def sample_questions():
    return [
        {
            "question_id": "Q1",
            "question": "Tell me about yourself.",
            "answer": "I completed my degree.",
            "answer_relevance": 80,
        },
        {
            "question_id": "Q2",
            "question": "Why this role?",
            "answer": "I enjoy working with data.",
            "answer_relevance": 90,
        },
    ]


def sample_result():
    return score_hr_interview(
        candidate_id="TEST-001",
        candidate_name="Test Candidate",
        role="Data Analyst",
        questions=sample_questions(),
        communication_score=80,
        confidence_score=75,
        consistency_score=85,
    )


class TestHRInterviewScoring(unittest.TestCase):

    def test_default_weights_sum_to_one(self):
        self.assertAlmostEqual(sum(DEFAULT_WEIGHTS.values()), 1.0)

    def test_custom_weights_are_normalized(self):
        weights = validate_weights({
            "answer_relevance": 4,
            "communication": 2,
            "confidence": 2,
            "consistency": 2,
        })
        self.assertAlmostEqual(sum(weights.values()), 1.0)
        self.assertAlmostEqual(weights["answer_relevance"], 0.4)

    def test_invalid_weights_rejected(self):
        with self.assertRaises(ValueError):
            validate_weights({
                "answer_relevance": -1,
                "communication": 1,
                "confidence": 1,
                "consistency": 1,
            })

    def test_invalid_score_rejected(self):
        with self.assertRaises(ValueError):
            validate_score(101, "test_score")

    def test_empty_question_list_rejected(self):
        with self.assertRaises(ValueError):
            normalize_interview_scores([])

    def test_question_scores_are_normalized(self):
        result = normalize_interview_scores(sample_questions())
        self.assertEqual(result["question_count"], 2)
        self.assertEqual(result["average_answer_relevance"], 85.0)

    def test_interview_score_is_between_zero_and_one_hundred(self):
        result = sample_result()
        score = result["final_hr_interview_score"]
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_weighted_breakdown_is_explainable(self):
        result = sample_result()
        self.assertIn("answer_relevance", result["weighted_breakdown"])
        self.assertIn(
            "weighted_contribution",
            result["weighted_breakdown"]["communication"],
        )

    def test_score_classification(self):
        self.assertEqual(classify_interview_score(90), "HIGH_SCORE")
        self.assertEqual(classify_interview_score(75), "GOOD_SCORE")
        self.assertEqual(classify_interview_score(60), "MODERATE_SCORE")
        self.assertEqual(classify_interview_score(30), "LOW_SCORE")

    def test_empty_candidate_id_rejected(self):
        with self.assertRaises(ValueError):
            score_hr_interview(
                candidate_id="",
                candidate_name="Candidate",
                role="Data Analyst",
                questions=sample_questions(),
                communication_score=80,
                confidence_score=70,
                consistency_score=80,
            )

    def test_report_files_are_created(self):
        result = sample_result()

        with tempfile.TemporaryDirectory() as directory:
            json_path, markdown_path = save_interview_report(
                [result],
                directory,
            )

            self.assertTrue(json_path.exists())
            self.assertTrue(markdown_path.exists())

            with json_path.open("r", encoding="utf-8") as file:
                report = json.load(file)

            self.assertEqual(report["total_candidates"], 1)

    def test_final_score_matches_weighted_components(self):
        result = sample_result()

        expected = sum(
            item["weighted_contribution"]
            for item in result["weighted_breakdown"].values()
        )

        self.assertAlmostEqual(
            result["final_hr_interview_score"],
            round(expected, 2),
        )


if __name__ == "__main__":
    unittest.main()
