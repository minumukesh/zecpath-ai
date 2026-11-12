import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(
    0,
    str(ROOT / "src")
)

from experience_parser import (
    parse_experience,
    calculate_total_experience,
    detect_gaps,
    detect_overlaps,
    calculate_relevance,
)


class TestExperienceParser(unittest.TestCase):

    def test_company_extraction(self):

        text = """
        Data Analyst
        ABC Analytics
        January 2022 - December 2023
        """

        experiences = parse_experience(text)

        self.assertEqual(
            len(experiences),
            1
        )

        self.assertEqual(
            experiences[0]["company"],
            "ABC Analytics"
        )


    def test_job_title_extraction(self):

        text = """
        Data Analyst
        ABC Analytics
        January 2022 - December 2023
        """

        experiences = parse_experience(text)

        self.assertEqual(
            experiences[0]["job_title"],
            "Data Analyst"
        )


    def test_duration_extraction(self):

        text = """
        Data Analyst
        ABC Analytics
        January 2022 - December 2023
        """

        experiences = parse_experience(text)

        self.assertGreater(
            experiences[0]["duration_months"],
            0
        )


    def test_total_experience(self):

        text = """
        Data Analyst
        ABC Analytics
        January 2022 - December 2023

        Business Analyst
        XYZ Solutions
        January 2024 - December 2024
        """

        experiences = parse_experience(text)

        total = calculate_total_experience(
            experiences
        )

        self.assertGreater(
            total["total_months"],
            0
        )


    def test_gap_detection(self):

        text = """
        Data Analyst
        ABC Company
        January 2020 - December 2020

        Data Analyst
        XYZ Company
        January 2022 - December 2022
        """

        experiences = parse_experience(text)

        gaps = detect_gaps(
            experiences
        )

        self.assertGreaterEqual(
            len(gaps),
            1
        )


    def test_overlap_detection(self):

        text = """
        Data Analyst
        ABC Company
        January 2022 - December 2023

        Business Analyst
        XYZ Company
        January 2023 - December 2023
        """

        experiences = parse_experience(text)

        overlaps = detect_overlaps(
            experiences
        )

        self.assertGreaterEqual(
            len(overlaps),
            1
        )


    def test_relevance_scoring(self):

        text = """
        Data Analyst
        ABC Analytics
        January 2022 - December 2023
        """

        experiences = parse_experience(text)

        result = calculate_relevance(
            experiences[0],
            "Data Analyst",
            [
                "python",
                "sql",
                "excel",
                "power bi",
            ]
        )

        self.assertGreater(
            result["relevance_score"],
            0
        )

        self.assertLessEqual(
            result["relevance_score"],
            1
        )


if __name__ == "__main__":
    unittest.main()
