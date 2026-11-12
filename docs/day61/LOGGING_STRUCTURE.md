# Day 61 - Logging Structure

## 1. Objective
Define a consistent logging structure across backend and AI services.

## 2. Standard Log Fields

| Field | Description |
|---|---|
| timestamp | Date and time of event |
| request_id | Unique request identifier |
| correlation_id | Identifier for tracing related service calls |
| service_name | Name of the service |
| log_level | INFO, WARNING, ERROR or DEBUG |
| event_type | Type of activity |
| status | Success, failure or processing |
| duration_ms | Processing duration |
| message | Event description |

## 3. API Logging
API logs should record incoming requests, endpoint information, response status and execution time.

Example JSON:

`json
{
  "timestamp": "2026-11-04T10:30:00Z",
  "request_id": "req_1001",
  "correlation_id": "corr_1001",
  "service_name": "resume_service",
  "log_level": "INFO",
  "event_type": "api_request",
  "status": "success",
  "duration_ms": 250,
  "message": "Resume request processed"
}
`",
",

Track model execution metadata:
- Model name.
- Model version.
- Request ID.
- Inference duration.
- Output status.
- Evaluation metadata.

Do not expose sensitive model inputs or candidate information unnecessarily.

## 5. Error Logging
Record error category, request ID, service name, timestamp and retry information.

Example error categories:
- ValidationError
- AuthenticationError
- ModelInferenceError
- DatabaseError
- TimeoutError
- ServiceUnavailableError

## 6. Log Levels

| Level | Purpose |
|---|---|
| DEBUG | Detailed debugging information |
| INFO | Normal application events |
| WARNING | Unexpected but recoverable conditions |
| ERROR | Failed operations |

## 7. Audit Log Structure
Audit records should include:
- audit_id
- actor_id
- action
- candidate_id or related record ID
- timestamp
- previous decision where applicable
- new decision where applicable
- reason or justification

Audit logs should be access-controlled and tamper-resistant.

## 8. Log Management
- Use structured JSON logging.
- Centralize logs from different services.
- Support searching by request_id.
- Define retention and archival policies.
- Restrict access to authorized personnel.
- Monitor logging failures.

## 9. Conclusion
This structure provides a consistent logging approach for API activity, AI model execution, errors and hiring decision audits.
