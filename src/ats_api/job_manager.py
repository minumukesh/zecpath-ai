import threading
import uuid
from datetime import datetime, timezone


class JobManager:

    def __init__(self):
        self.jobs = {}
        self.lock = threading.Lock()

    def create_job(self, job_type, payload=None):

        job_id = str(uuid.uuid4())

        job = {
            "job_id": job_id,
            "job_type": job_type,
            "status": "queued",
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "payload": payload or {},
            "result": None,
            "error": None
        }

        with self.lock:
            self.jobs[job_id] = job

        return job_id

    def update_job(
        self,
        job_id,
        status,
        result=None,
        error=None
    ):

        with self.lock:

            if job_id not in self.jobs:
                return False

            self.jobs[job_id]["status"] = status
            self.jobs[job_id]["result"] = result
            self.jobs[job_id]["error"] = error

        return True

    def get_job(self, job_id):

        with self.lock:

            if job_id not in self.jobs:
                return None

            return dict(self.jobs[job_id])


job_manager = JobManager()
