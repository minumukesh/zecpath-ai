import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from resume_section_classifier.classifier import classify_resume


class TestResumeSectionClassifier(unittest.TestCase):

    def test_standard_headings(self):
        text = """
        SKILLS
        Python, SQL

        WORK EXPERIENCE
        Data Analyst
        ABC Technologies
        2024 - 2025

        EDUCATION
        MCA
        XYZ University

        CERTIFICATIONS
        IBM Python for Data Science

        PROJECTS
        Sales Dashboard
        """

        result = classify_resume(text)

        self.assertTrue(result["skills"])
        self.assertTrue(result["work_experience"])
        self.assertTrue(result["education"])
        self.assertTrue(result["certifications"])
        self.assertTrue(result["projects"])

    def test_heading_variations(self):
        text = """
        TECHNICAL COMPETENCIES
        Python, SQL, Power BI

        PROFESSIONAL BACKGROUND
        Data Analyst
        ABC Technologies
        2023 - Present

        ACADEMIC QUALIFICATIONS
        Bachelor of Computer Applications

        PROFESSIONAL CERTIFICATIONS
        Google Data Analytics

        ACADEMIC PROJECTS
        Customer Churn Prediction
        """

        result = classify_resume(text)

        self.assertTrue(result["skills"])
        self.assertTrue(result["work_experience"])
        self.assertTrue(result["education"])
        self.assertTrue(result["certifications"])
        self.assertTrue(result["projects"])

    def test_missing_headings(self):
        text = """
        Python
        SQL
        Excel
        Power BI

        Data Analyst
        DataWorks Technologies
        2022 - 2024

        MCA
        ABC University
        2024 - 2026

        Certified Data Analyst
        Coursera
        2025

        Sales Forecasting Dashboard
        Built a forecasting dashboard using Python and Power BI.
        """

        result = classify_resume(text)

        self.assertTrue(result["skills"])
        self.assertTrue(result["work_experience"])
        self.assertTrue(result["education"])
        self.assertTrue(result["certifications"])
        self.assertTrue(result["projects"])


if __name__ == "__main__":
    unittest.main()