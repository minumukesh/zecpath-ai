import unittest

from src.resume_extraction.text_cleaner import clean_text, normalize_bullets


class TestResumeExtraction(unittest.TestCase):

    def test_bullets(self):
        newline = chr(10)

        text = (
            chr(0x2022) + " Python"
            + newline
            + chr(0x25CF) + " SQL"
            + newline
            + chr(0x25AA) + " Excel"
        )

        result = normalize_bullets(text)

        expected = (
            "- Python"
            + newline
            + "- SQL"
            + newline
            + "- Excel"
        )

        self.assertEqual(result, expected)


    def test_heading(self):
        result = clean_text("technical skills:")

        self.assertEqual(
            result,
            "TECHNICAL SKILLS"
        )


    def test_spaces(self):
        newline = chr(10)

        text = (
            "John    Smith"
            + newline
            + newline
            + newline
            + "Python     SQL"
        )

        result = clean_text(text)

        expected = (
            "John Smith"
            + newline
            + newline
            + "Python SQL"
        )

        self.assertEqual(result, expected)


    def test_empty_text(self):
        result = clean_text("")

        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()