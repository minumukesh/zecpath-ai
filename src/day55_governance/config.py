"""Security and governance configuration."""

RETENTION_POLICIES = {
    "transcripts": 90,
    "reports": 365,
    "audit_logs": 730
}

ROLES = {
    "admin": [
        "audit.read",
        "audit.verify",
        "consent.read",
        "consent.manage",
        "transcript.read",
        "transcript.write",
        "transcript.delete",
        "report.read",
        "report.write",
        "report.delete",
        "retention.manage"
    ],
    "hr_manager": [
        "consent.read",
        "transcript.read",
        "report.read",
        "report.write"
    ],
    "interviewer": [
        "consent.read",
        "transcript.read",
        "transcript.write"
    ],
    "auditor": [
        "audit.read",
        "audit.verify",
        "report.read"
    ]
}

ALLOWED_DATA_CATEGORIES = {
    "transcripts",
    "reports"
}
