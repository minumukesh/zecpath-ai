import re

POSITIVE_WORDS = {
    "good", "great", "excellent", "positive", "happy",
    "confident", "success", "successful", "achieved",
    "improved", "improvement", "enjoy", "enjoyed",
    "love", "like", "motivated", "excited", "strong",
    "effective", "helpful", "proud", "comfortable",
    "capable", "skilled", "teamwork", "collaborate",
    "completed", "solved", "learned", "best",
}

NEGATIVE_WORDS = {
    "bad", "poor", "negative", "sad", "angry",
    "failed", "failure", "difficult", "problem",
    "problems", "weak", "hate", "worried", "upset",
    "stress", "stressed", "confused", "unhappy",
    "unable", "worst", "mistake", "struggle",
    "struggled", "disappointed", "frustrated",
}


def _count_matches(text, vocabulary):
    tokens = re.findall(
        r"\b[a-zA-Z]+\b",
        str(text or "").lower()
    )

    return sum(
        1 for token in tokens
        if token in vocabulary
    )


def analyze_sentiment(text):
    text = str(text or "").strip()

    positive_count = _count_matches(
        text,
        POSITIVE_WORDS
    )

    negative_count = _count_matches(
        text,
        NEGATIVE_WORDS
    )

    total = positive_count + negative_count

    if total == 0:
        sentiment = "NEUTRAL"
        score = 0.0
    else:
        score = round(
            (positive_count - negative_count) / total,
            4
        )

        if score > 0:
            sentiment = "POSITIVE"
        elif score < 0:
            sentiment = "NEGATIVE"
        else:
            sentiment = "NEUTRAL"

    return {
        "sentiment": sentiment,
        "sentiment_score": score,
        "positive_word_count": positive_count,
        "negative_word_count": negative_count,
        "method": "lexicon_based",
    }
