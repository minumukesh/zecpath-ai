# Day 55 - Security Framework

## Security Controls

| Control | Implementation |
|---|---|
| Audit logging | JSONL event records |
| Audit integrity | SHA-256 hash chain |
| Score logging | Score and model identifier |
| Decision logging | Decision and explanation |
| Consent | Purpose-based consent records |
| Transcript storage | Separate protected directory |
| Report storage | Separate protected directory |
| Access control | Role-based permissions |
| Retention | Configured expiry for transcripts and reports |
| Human oversight | Decision log records review requirement |

## Roles

Admin, HR Manager, Interviewer and Auditor have separate permissions.

## Threats considered

- Unauthorized data access.
- Unconsented candidate data processing.
- Audit record modification.
- Excessive data retention.
- Unauthorized report access.
- Untraceable hiring decisions.

## Limitations

Application-level role checks are not a replacement for authenticated identity management. Hash chaining detects modification but does not prevent deletion or rewriting by an attacker with full file access. Encryption at rest and production identity controls remain deployment requirements.
