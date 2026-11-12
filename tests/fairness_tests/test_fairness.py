import unittest

from src.fairness_normalization import (
    normalize_whitespace,
    normalize_sections,
    mask_personal_attributes,
    normalize_resume,
    normalize_component_scores,
    reduce_keyword_dependence,
    calculate_bias_indicators,
    compare_scores,
    generate_fairness_evaluation,
)


class TestFairnessNormalization(unittest.TestCase):

    def test_whitespace_normalization(self):
        text = "Python    SQL\n\n\nPower BI"
        result = normalize_whitespace(text)

        self.assertEqual(
            result,
            "Python SQL\nPower BI"
        )

    def test_section_normalization(self):
        text = (
            "Professional Experience\n"
            "Data Analyst\n"
            "Academic Background\n"
            "B.Tech"
        )

        result = normalize_sections(text)

        self.assertIn(
            "WORK EXPERIENCE",
            result
        )

        self.assertIn(
            "EDUCATION",
            result
        )

    def test_personal_attribute_masking(self):
        text = (
            "Email: test@example.com\n"
            "Phone: +91 9876543210\n"
            "Gender: Male"
        )

        masked, fields = mask_personal_attributes(text)

        self.assertNotIn(
            "test@example.com",
            masked
        )

        self.assertIn(
            "email",
            fields
        )

        self.assertIn(
            "phone",
            fields
        )

        self.assertIn(
            "gender",
            fields
        )

    def test_resume_normalization(self):
        text = (
            "Jane Doe\n"
            "Email: jane@example.com\n"
            "Skills\nPython SQL"
        )

        result = normalize_resume(text)

        self.assertTrue(
            result["normalization_applied"]
        )

        self.assertIn(
            "email",
            result["masked_attributes"]
        )

    def test_score_normalization(self):
        scores = {
            "skill": 1.5,
            "experience": -0.2,
            "education": 0.8,
        }

        result = normalize_component_scores(scores)

        self.assertEqual(
            result["skill"],
            1.0
        )

        self.assertEqual(
            result["experience"],
            0.0
        )

        self.assertEqual(
            result["education"],
            0.8
        )

    def test_keyword_dependence_reduction(self):
        result = reduce_keyword_dependence(
            keyword_score=1.0,
            semantic_score=0.5,
            experience_score=0.5,
            education_score=0.5,
        )

        self.assertLess(
            result,
            1.0
        )

        self.assertGreater(
            result,
            0.0
        )

    def test_bias_indicators(self):
        result = calculate_bias_indicators(
            original_score=80,
            normalized_score=0.70,
            keyword_score=0.95,
            semantic_score=0.40,
            masked_attributes=["email"],
        )

        self.assertIn(
            "HIGH_KEYWORD_DEPENDENCE",
            result["indicators"]
        )

        self.assertIn(
            "PERSONAL_ATTRIBUTES_MASKED",
            result["indicators"]
        )

    def test_score_comparison(self):
        result = compare_scores(
            80,
            75
        )

        self.assertEqual(
            result["difference"],
            -5.0
        )

    def test_fairness_evaluation(self):
        result = generate_fairness_evaluation(
            candidate_name="Test Candidate",
            original_score=80,
            keyword_score=0.80,
            semantic_score=0.85,
            experience_score=0.80,
            education_score=0.75,
            masked_attributes=["email"],
        )

        self.assertIn(
            "fairness_adjusted_score",
            result
        )

        self.assertIn(
            "bias_evaluation",
            result
        )

        self.assertIn(
            "masked_attributes",
            result
        )

        self.assertIn(
            "weights",
            result
        )


if __name__ == "__main__":
    unittest.main()
