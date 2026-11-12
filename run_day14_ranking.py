import json
from pathlib import Path

from src.candidate_ranking import generate_ranking_output


INPUT_FILE = Path("outputs/day13/candidate_scores.json")
OUTPUT_DIR = Path("outputs/day14")
OUTPUT_FILE = OUTPUT_DIR / "ranked_candidates.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Day 13 input file not found: {INPUT_FILE}"
    )

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    candidates = json.load(file)

ranking_output = generate_ranking_output(
    candidates,
    top_n=5
)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(
        ranking_output,
        file,
        indent=2
    )

print("DAY 14 CANDIDATE RANKING COMPLETED")
print()
print(f"Total candidates: {ranking_output['total_candidates']}")
print(
    f"Shortlist threshold: "
    f"{ranking_output['shortlist_threshold']}"
)
print(
    f"Review threshold: "
    f"{ranking_output['review_threshold']}"
)
print()

print("RANKED CANDIDATES:")
for candidate in ranking_output["ranked_candidates"]:
    print(
        f"Rank {candidate['rank']}: "
        f"{candidate['candidate_name']} | "
        f"{candidate['ats_score']} | "
        f"{candidate['decision']}"
    )

print()
print(
    f"Shortlisted: "
    f"{len(ranking_output['shortlisted_candidates'])}"
)
print(
    f"Review: "
    f"{len(ranking_output['review_candidates'])}"
)
print(
    f"Auto-rejected: "
    f"{len(ranking_output['auto_rejected_candidates'])}"
)

print()
print(f"Output saved to: {OUTPUT_FILE}")
