"""Local demonstration HTTP API. Not production hardened."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .technical_engine import TechnicalInterviewEngine
from .hr_engine import HRInterviewEngine

technical_engine = TechnicalInterviewEngine()
hr_engine = HRInterviewEngine()

class InterviewAPIHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            raise ValueError("Request body is required.")
        return json.loads(self.rfile.read(length).decode("utf-8-sig"))

    def do_GET(self):
        if self.path == "/health":
            return self.send_json(200, {"service": "Zecpath Interview API", "status": "running"})
        if self.path == "/api/v1/interviews/technical/roles":
            return self.send_json(200, {"roles": ["mern", "java", "devops"]})
        return self.send_json(404, {"error": "Endpoint not found."})

    def do_POST(self):
        try:
            data = self.read_json()
            if self.path == "/api/v1/interviews/technical/blueprint":
                result = technical_engine.get_interview_blueprint(
                    data["role"], data["experience_years"]
                )
                return self.send_json(200, result)
            if self.path == "/api/v1/interviews/hr/evaluate":
                result = hr_engine.evaluate_candidate(
                    data["candidate_id"],
                    data["candidate_name"],
                    data["role"],
                    data["scores"],
                    data.get("manager_feedback", "")
                )
                return self.send_json(200, result)
            return self.send_json(404, {"error": "Endpoint not found."})
        except (KeyError, ValueError, TypeError, json.JSONDecodeError) as exc:
            return self.send_json(400, {"error": str(exc)})

    def log_message(self, format, *args):
        return

def start_server(host="127.0.0.1", port=8000):
    server = ThreadingHTTPServer((host, port), InterviewAPIHandler)
    print(f"Zecpath Interview API running at http://{host}:{port}")
    print("Press CTRL+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nAPI server stopped.")
    finally:
        server.server_close()

if __name__ == "__main__":
    start_server()