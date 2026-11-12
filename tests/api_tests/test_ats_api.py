import time
import unittest

from fastapi.testclient import TestClient

from src.ats_api.api import app


class TestATSAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get(
            "/api/v1/health"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.json()["status"],
            "healthy"
        )

    def test_resume_upload(self):
        response = self.client.post(
            "/api/v1/resumes/upload",
            files={
                "file": (
                    "resume.txt",
                    b"Skills:\nPython\nSQL\n",
                    "text/plain"
                )
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertIn(
            "resume_id",
            response.json()
        )

    def test_invalid_file_type(self):
        response = self.client.post(
            "/api/v1/resumes/upload",
            files={
                "file": (
                    "resume.pdf",
                    b"PDF content",
                    "application/pdf"
                )
            }
        )

        self.assertEqual(
            response.status_code,
            415
        )

        self.assertEqual(
            response.json()["detail"]["error_code"],
            "UNSUPPORTED_FILE_TYPE"
        )

    def test_parse_resume_async(self):
        upload = self.client.post(
            "/api/v1/resumes/upload",
            files={
                "file": (
                    "parse_test.txt",
                    b"Skills:\nPython\nSQL\nEducation:\nB.Tech",
                    "text/plain"
                )
            }
        )

        self.assertEqual(
            upload.status_code,
            200
        )

        resume_id = upload.json()["resume_id"]

        response = self.client.post(
            f"/api/v1/resumes/{resume_id}/parse",
            json={
                "resume_id": resume_id
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.json()["status"],
            "queued"
        )

        job_id = response.json()["job_id"]

        time.sleep(0.2)

        job = self.client.get(
            f"/api/v1/jobs/{job_id}"
        )

        self.assertEqual(
            job.status_code,
            200
        )

        self.assertIn(
            job.json()["status"],
            ["running", "completed"]
        )

    def test_score_resume_async(self):
        upload = self.client.post(
            "/api/v1/resumes/upload",
            files={
                "file": (
                    "score_test.txt",
                    b"Skills:\nPython\nSQL\nMachine Learning\nData Analysis",
                    "text/plain"
                )
            }
        )

        resume_id = upload.json()["resume_id"]

        response = self.client.post(
            f"/api/v1/resumes/{resume_id}/score",
            json={
                "resume_id": resume_id,
                "job_id": "JOB-001",
                "role": "Data Analyst"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.json()["status"],
            "queued"
        )

        job_id = response.json()["job_id"]

        time.sleep(0.2)

        job = self.client.get(
            f"/api/v1/jobs/{job_id}"
        )

        self.assertEqual(
            job.status_code,
            200
        )

        self.assertIn(
            job.json()["status"],
            ["running", "completed"]
        )

    def test_shortlisting(self):
        response = self.client.post(
            "/api/v1/jobs/JOB-001/shortlist",
            json={
                "candidates": [
                    {
                        "candidate_id": "C001",
                        "score": 85
                    },
                    {
                        "candidate_id": "C002",
                        "score": 65
                    },
                    {
                        "candidate_id": "C003",
                        "score": 40
                    }
                ]
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.json()

        self.assertEqual(
            len(data["shortlisted"]),
            1
        )

        self.assertEqual(
            len(data["review"]),
            1
        )

        self.assertEqual(
            len(data["rejected"]),
            1
        )

    def test_invalid_shortlist_thresholds(self):
        response = self.client.post(
            "/api/v1/jobs/JOB-002/shortlist",
            json={
                "candidates": [
                    {
                        "candidate_id": "C001",
                        "score": 80
                    }
                ],
                "shortlist_threshold": 50,
                "review_threshold": 70
            }
        )

        self.assertEqual(
            response.status_code,
            400
        )

        self.assertEqual(
            response.json()["detail"]["error_code"],
            "INVALID_THRESHOLDS"
        )

    def test_missing_job(self):
        response = self.client.get(
            "/api/v1/jobs/does-not-exist"
        )

        self.assertEqual(
            response.status_code,
            404
        )

        self.assertEqual(
            response.json()["detail"]["error_code"],
            "JOB_NOT_FOUND"
        )


if __name__ == "__main__":
    unittest.main()
