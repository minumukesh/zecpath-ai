# Day 55 - Security & AI Governance

## Objective
Ensure the AI system is secure, auditable and compliant.

## 1. Audit Trail System

The governance module records:
- Score generation events.
- Hiring decision events.
- Consent events.
- Data storage and access events.
- Data deletion events.
- Retention deletion events.

Each audit record includes a timestamp, actor, event type, resource, details and previous-record hash.

SHA-256 hash chaining allows the audit sequence to be checked for accidental or unauthorized modification.

The audit log is stored in JSON Lines format.

## 2. Data Retention Policies

| Data category | Demonstration retention |
|---|---:|
| Interview transcripts | 90 days |
| Reports | 365 days |
| Audit logs | 730 days |

Transcript and report retention is enforced by the retention routine.

Audit-log retention is documented as a policy but automatic audit-log deletion is not implemented. Audit logs should not be deleted without an approved legal and security process.

These durations are demonstration settings, not universal legal requirements.

## 3. Consent-Based Data Usage

The system records:
- Candidate identifier.
- Purpose of data processing.
- Consent decision.
- Timestamp.
- Actor recording consent.

The latest consent record controls whether data can be stored or read.

Storage is rejected if the candidate has not granted consent for the specified purpose.

## 4. Secure Storage

Separate storage locations are used for:
- Interview transcripts.
- Interview reports.
- Consent records.
- Audit records.

JSON writes use temporary files followed by atomic replacement.

Windows folder permissions must be configured separately. This demonstration does not provide encryption at rest.

## 5. Access Control

| Role | Main permissions |
|---|---|
| Admin | Full governance management |
| HR Manager | Read consent, reports and transcripts; write reports |
| Interviewer | Read and write transcripts |
| Auditor | Read and verify audit logs; read reports |

The application checks role permissions before protected operations.

## 6. Security Framework

- Authentication must identify the actual user before assigning an application role.
- Authorization follows role-based access control.
- Consent is checked before protected data usage.
- Audit events record important operations.
- Hash chaining detects audit-log modification.
- Retention routines remove expired transcripts and reports.
- Human review is required for hiring decisions.

## 7. Limitations and Production Requirements

This is a local governance demonstration.

Before production:
- Integrate enterprise authentication and identity management.
- Use encrypted storage and managed encryption keys.
- Restrict folder and database permissions.
- Protect audit logs with a separate append-only service.
- Define legally approved retention schedules.
- Add backup and disaster recovery.
- Conduct penetration testing and security review.
- Verify applicable privacy and employment regulations.

The module is not a legal compliance certification.
