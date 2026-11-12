import unittest

from src.jd_parser.extractor import (
    extract_skills,
    extract_role,
    extract_experience,
    extract_education
)


class TestJDParser(unittest.TestCase):

    def test_skills(self):

        text = """
        We need a Data Analyst with Python,
        SQL, Excel and Power BI.
        """

        skills = extract_skills(text)

        self.assertIn("python", skills)
        self.assertIn("sql", skills)
        self.assertIn("excel", skills)
        self.assertIn("power bi", skills)


    def test_role(self):

        text = "We are hiring a Data Analyst."

        role = extract_role(text)

        self.assertEqual(
            role,
            "data analyst"
        )


    def test_experience(self):

        text = "Minimum 2 years of experience required."

        experience = extract_experience(text)

        self.assertEqual(
            experience["minimum_years"],
            2
        )


    def test_education(self):

        text = "Bachelor degree in Computer Science required."

        education = extract_education(text)

        self.assertIn(
            "bachelor",
            education
        )


if __name__ == "__main__":
    unittest.main()
