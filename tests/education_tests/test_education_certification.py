import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(
    0,
    str(ROOT / "src")
)

from education_certification import (
    extract_education,
    extract_certifications,
    education_relevance,
)


class TestEducationCertification(unittest.TestCase):

    # ---------------------------------------------------------
    # 1. DEGREE TYPE EXTRACTION
    # ---------------------------------------------------------

    def test_degree_extraction(self):

        text = """
        B.Tech in Computer Science Engineering
        ABC University
        2022
        """

        result = extract_education(text)

        self.assertEqual(len(result), 1)

        self.assertEqual(
            result[0]["degree"],
            "Bachelor of Technology"
        )

    # ---------------------------------------------------------
    # 2. FIELD OF STUDY EXTRACTION
    # ---------------------------------------------------------

    def test_field_extraction(self):

        text = """
        B.Tech in Computer Science Engineering
        ABC University
        2022
        """

        result = extract_education(text)

        self.assertEqual(
            result[0]["field_of_study"],
            "Computer Science"
        )

    # ---------------------------------------------------------
    # 3. INSTITUTION EXTRACTION
    # ---------------------------------------------------------

    def test_institution_extraction(self):

        text = """
        B.Tech in Computer Science
        ABC University
        2022
        """

        result = extract_education(text)

        self.assertEqual(
            result[0]["institution"],
            "ABC University"
        )

    # ---------------------------------------------------------
    # 4. GRADUATION YEAR EXTRACTION
    # ---------------------------------------------------------

    def test_graduation_year(self):

        text = """
        B.Tech in Computer Science
        ABC University
        2022
        """

        result = extract_education(text)

        self.assertEqual(
            result[0]["graduation_year"],
            2022
        )

    # ---------------------------------------------------------
    # 5. CERTIFICATION EXTRACTION
    # ---------------------------------------------------------

    def test_certification_extraction(self):

        text = """
        CERTIFICATIONS

        Google Data Analytics Certificate
        AWS Certified Cloud Practitioner
        """

        result = extract_certifications(text)

        self.assertGreaterEqual(
            len(result),
            2
        )

    # ---------------------------------------------------------
    # 6. CERTIFICATION CATEGORY
    # ---------------------------------------------------------

    def test_certification_category(self):

        text = """
        CERTIFICATIONS

        AWS Certified Cloud Practitioner
        Python Programming Certificate
        """

        result = extract_certifications(text)

        categories = {
            item["category"]
            for item in result
        }

        self.assertIn(
            "Cloud",
            categories
        )

        self.assertIn(
            "Programming",
            categories
        )

    # ---------------------------------------------------------
    # 7. EDUCATION RELEVANCE
    # ---------------------------------------------------------

    def test_education_relevance(self):

        education = [
            {
                "degree": "Bachelor of Technology",
                "field_of_study": "Computer Science",
                "institution": "ABC University",
                "graduation_year": 2022,
            }
        ]

        result = education_relevance(
            education,
            "Data Analyst"
        )

        self.assertGreater(
            result["score"],
            0
        )

        self.assertLessEqual(
            result["score"],
            1
        )

    # ---------------------------------------------------------
    # 8. NAMING NORMALIZATION
    # ---------------------------------------------------------

    def test_naming_normalization(self):

        text = """
        BSc in CSE
        XYZ College
        2023
        """

        result = extract_education(text)

        self.assertEqual(
            result[0]["degree"],
            "Bachelor of Science"
        )

        self.assertEqual(
            result[0]["field_of_study"],
            "Computer Science"
        )

    # ---------------------------------------------------------
    # 9. STRUCTURED ACADEMIC PROFILE
    # ---------------------------------------------------------

    def test_structured_academic_profile(self):

        text = """
        MCA in Computer Science
        XYZ University
        2025
        """

        result = extract_education(text)

        profile = result[0]

        required_fields = {
            "degree",
            "field_of_study",
            "institution",
            "graduation_year",
        }

        self.assertTrue(
            required_fields.issubset(
                profile.keys()
            )
        )

        self.assertEqual(
            profile["degree"],
            "Master of Computer Applications"
        )

        self.assertEqual(
            profile["field_of_study"],
            "Computer Science"
        )

        self.assertEqual(
            profile["institution"],
            "XYZ University"
        )

        self.assertEqual(
            profile["graduation_year"],
            2025
        )


if __name__ == "__main__":
    unittest.main()