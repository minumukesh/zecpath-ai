SHORTLIST_THRESHOLD = 70.0
REVIEW_THRESHOLD = 50.0


def classify_candidate(score):
    """Classify candidate based on ATS score."""

    score = float(score or 0)

    if score >= SHORTLIST_THRESHOLD:
        return "SHORTLIST"

    if score >= REVIEW_THRESHOLD:
        return "REVIEW"

    return "AUTO-REJECT"


def rank_candidates(candidates):
    """Sort candidates by ATS score in descending order."""

    ranked = sorted(
        candidates,
        key=lambda candidate: float(candidate.get("ats_score", 0) or 0),
        reverse=True
    )

    for index, candidate in enumerate(ranked, start=1):
        candidate["rank"] = index
        candidate["decision"] = classify_candidate(
            candidate.get("ats_score", 0)
        )

    return ranked


def shortlist_candidates(
    candidates,
    threshold=SHORTLIST_THRESHOLD
):
    """Return candidates meeting the shortlist threshold."""

    return [
        candidate
        for candidate in candidates
        if float(candidate.get("ats_score", 0) or 0) >= threshold
    ]


def review_candidates(candidates):
    """Return candidates in the recruiter review zone."""

    return [
        candidate
        for candidate in candidates
        if REVIEW_THRESHOLD
        <= float(candidate.get("ats_score", 0) or 0)
        < SHORTLIST_THRESHOLD
    ]


def auto_reject_candidates(candidates):
    """Return candidates below the review threshold."""

    return [
        candidate
        for candidate in candidates
        if float(candidate.get("ats_score", 0) or 0)
        < REVIEW_THRESHOLD
    ]


def get_top_candidates(candidates, top_n=5):
    """Return the top N ranked candidates."""

    ranked = rank_candidates(candidates)

    return ranked[:top_n]


def generate_ranking_output(candidates, top_n=5):
    """Generate complete recruiter-friendly ranking output."""

    ranked = rank_candidates(candidates)

    shortlisted = shortlist_candidates(ranked)
    review = review_candidates(ranked)
    rejected = auto_reject_candidates(ranked)

    return {
        "total_candidates": len(ranked),
        "shortlist_threshold": SHORTLIST_THRESHOLD,
        "review_threshold": REVIEW_THRESHOLD,
        "ranked_candidates": ranked,
        "top_candidates": ranked[:top_n],
        "shortlisted_candidates": shortlisted,
        "review_candidates": review,
        "auto_rejected_candidates": rejected
    }
