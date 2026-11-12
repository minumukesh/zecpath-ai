import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from skill_extraction import extract_skills


class TestSkillExtraction(unittest.TestCase):

    def test_direct_skills(self):
        text = "Python, SQL, Excel, Power BI, Machine Learning"

        skills = extract_skills(text)
        names = {item["skill"] for item in skills}

        self.assertIn("python", names)
        self.assertIn("sql", names)
        self.assertIn("excel", names)
        self.assertIn("power bi", names)
        self.assertIn("machine learning", names)

    def test_synonyms(self):
        text = "Python3, PowerBI, ReactJS, NodeJS, Mongo DB"

        skills = extract_skills(text)
        names = {item["skill"] for item in skills}

        self.assertIn("python", names)
        self.assertIn("power bi", names)
        self.assertIn("react", names)
        self.assertIn("node.js", names)
        self.assertIn("mongodb", names)

    def test_mern_stack(self):
        text = "Experienced MERN stack developer."

        skills = extract_skills(text)
        names = {item["skill"] for item in skills}

        self.assertIn("mongodb", names)
        self.assertIn("express.js", names)
        self.assertIn("react", names)
        self.assertIn("node.js", names)

    def test_confidence_scores(self):
        text = "Python SQL Power BI"

        skills = extract_skills(text)

        self.assertTrue(
            all(
                0 <= item["confidence"] <= 1
                for item in skills
            )
        )

    def test_deduplication(self):
        text = "Python Python3 Python"

        skills = extract_skills(text)

        python_count = sum(
            item["skill"] == "python"
            for item in skills
        )

        self.assertEqual(python_count, 1)


if __name__ == "__main__":
    unittest.main()
