import json
import subprocess
import sys
import time
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8765"

def request(path, method="GET", payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        return response.status, json.loads(response.read().decode("utf-8"))

def main():
    process = subprocess.Popen(
        [sys.executable, "-c",
         "from src.interview_system.api import start_server; start_server(port=8765)"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    try:
        for _ in range(30):
            if process.poll() is not None:
                raise RuntimeError("API process stopped before becoming ready.")
            try:
                status, body = request("/health")
                break
            except Exception:
                time.sleep(0.3)
        else:
            raise RuntimeError("API did not become ready.")

        assert status == 200 and body["status"] == "running"
        print("PASS GET /health")

        status, body = request("/api/v1/interviews/technical/roles")
        assert status == 200 and set(body["roles"]) == {"mern", "java", "devops"}
        print("PASS GET /api/v1/interviews/technical/roles")

        status, body = request(
            "/api/v1/interviews/technical/blueprint", "POST",
            {"role": "mern", "experience_years": 5}
        )
        assert status == 200 and body["experience_level"] == "advanced"
        assert all(k in body["sections"] for k in ("introduction", "experience", "conceptual", "scenario"))
        print("PASS POST /api/v1/interviews/technical/blueprint")

        status, body = request(
            "/api/v1/interviews/hr/evaluate", "POST",
            {
                "candidate_id": "API001",
                "candidate_name": "API Candidate",
                "role": "Analyst",
                "scores": {
                    "communication": 80,
                    "role_understanding": 80,
                    "problem_solving": 80,
                    "professionalism": 80
                },
                "manager_feedback": "API smoke test"
            }
        )
        assert status == 200 and body["score"] == 80
        print("PASS POST /api/v1/interviews/hr/evaluate")
        print("\nAll four API smoke tests passed.")
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

if __name__ == "__main__":
    main()
