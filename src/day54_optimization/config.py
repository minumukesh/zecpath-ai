"""Day 54 optimization configuration."""

DEFAULT_THRESHOLD = 0.65

THRESHOLD_CANDIDATES = [
    0.40, 0.45, 0.50, 0.55, 0.60,
    0.65, 0.70, 0.75, 0.80, 0.85
]

INTENT_KEYWORDS = {
    "accept": [
        "yes", "accept", "agree", "continue",
        "proceed", "okay", "ok"
    ],
    "reject": [
        "no", "reject", "decline", "stop",
        "cancel", "refuse"
    ],
    "clarification": [
        "repeat", "explain", "clarify",
        "what do you mean", "not understand"
    ],
    "question": [
        "what", "why", "how", "when",
        "where", "which"
    ]
}

CONSISTENCY_RANGE_LIMIT = 15.0
