import unittest

from src.candidate_ranking import (
    classify_candidate,
    rank_candidates,
    shortlist_candidates,
    review_candidates,
    auto_reject_candidates,
    get_top_candidates,
    generate_ranking_output,
)


class TestCandidateRanking(unittest.TestCase):

    def setUp(self):
        self.candidates = [
            {
                "candidate_name": "Candidate A",
                "role": "Data Analyst",
                "ats_score": 82.0,
            },
            {
                "candidate_name": "Candidate B",
                "role": "Data Analyst",
                "ats_score": 68.0,
            },
            {
                "candidate_name": "Candidate C",
                "role": "Data Analyst",
                "ats_score": 45.0,
            },
            {
                "candidate_name": "Candidate D",
                "role": "Data Analyst",
                "ats_score": 91.0,
            },
        ]

    def test_classification(self):
        self.assertEqual(
            classify_candidate(80),
            "SHORTLIST"
        )

        self.assertEqual(
            classify_candidate(70),
            "SHORTLIST"
        )

        self.assertEqual(
            classify_candidate(60),
            "REVIEW"
        )

        self.assertEqual(
            classify_candidate(50),
            "REVIEW"
        )

        self.assertEqual(
            classify_candidate(40),
            "AUTO-REJECT"
        )

    def test_ranking(self):
        ranked = rank_candidates(self.candidates)

        self.assertEqual(
            ranked[0]["candidate_name"],
            "Candidate D"
        )

        self.assertEqual(
            ranked[0]["rank"],
            1
        )

        self.assertEqual(
            ranked[-1]["candidate_name"],
            "Candidate C"
        )

    def test_shortlisting(self):
        shortlisted = shortlist_candidates(self.candidates)

        self.assertEqual(len(shortlisted), 2)

    def test_review_zone(self):
        review = review_candidates(self.candidates)

        self.assertEqual(len(review), 1)
        self.assertEqual(
            review[0]["candidate_name"],
            "Candidate B"
        )

    def test_auto_reject(self):
        rejected = auto_reject_candidates(self.candidates)

        self.assertEqual(len(rejected), 1)
        self.assertEqual(
            rejected[0]["candidate_name"],
            "Candidate C"
        )

    def test_top_candidates(self):
        top = get_top_candidates(
            self.candidates,
            top_n=2
        )

        self.assertEqual(len(top), 2)
        self.assertEqual(
            top[0]["candidate_name"],
            "Candidate D"
        )
        self.assertEqual(
            top[1]["candidate_name"],
            "Candidate A"
        )

    def test_recruiter_output(self):
        output = generate_ranking_output(
            self.candidates,
            top_n=3
        )

        self.assertIn(
            "ranked_candidates",
            output
        )

        self.assertIn(
            "top_candidates",
            output
        )

        self.assertIn(
            "shortlisted_candidates",
            output
        )

        self.assertIn(
            "review_candidates",
            output
        )

        self.assertIn(
            "auto_rejected_candidates",
            output
        )

        self.assertEqual(
            output["total_candidates"],
            4
        )


if __name__ == "__main__":
    unittest.main()
