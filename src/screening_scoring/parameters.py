SCORING_WEIGHTS = {
    "clarity": 0.25,
    "relevance": 0.35,
    "completeness": 0.25,
    "consistency": 0.15,
}

SCORE_MIN = 0.0
SCORE_MAX = 100.0

PARAMETER_DESCRIPTIONS = {
    "clarity": "Measures how understandable the answer is.",
    "relevance": "Measures how closely the answer addresses the question.",
    "completeness": "Measures whether the requested information is present.",
    "consistency": "Measures consistency with other candidate responses.",
}
