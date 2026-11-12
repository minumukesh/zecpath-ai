# Zecpath AI ATS Scoring Logic

## 1. Purpose

The ATS scoring engine provides a transparent and explainable candidate
score.

Implementation:

src/ats_scoring/engine.py

## 2. Scoring Components

The ATS score uses four components:

1. Skill Match
2. Experience Relevance
3. Education Alignment
4. Semantic Similarity

## 3. Role-Based Weights

| Role | Skills | Experience | Education | Semantic |
|---|---:|---:|---:|---:|
| Data Analyst | 40% | 25% | 15% | 20% |
| Software Developer | 45% | 30% | 10% | 15% |
| ML Engineer | 45% | 30% | 10% | 15% |
| Business Analyst | 45% | 30% | 10% | 15% |
| Default | 40% | 25% | 15% | 20% |

## 4. Formula

Each component is normalized to a value between 0 and 1.

Weighted Score =
Sum of (Normalized Component Score x Component Weight)

The weighted result is converted to a 0-100 ATS score.

## 5. Missing Data

The scoring engine handles missing information.

Rules:

- Missing or invalid values are normalized safely.
- Missing components are recorded.
- Missing components are excluded from active weighting.
- Remaining weights are normalized.
- If all components are missing, the ATS score becomes 0.

## 6. Day 13 Classification

| ATS Score | Classification |
|---:|---|
| 85-100 | Excellent Match |
| 70-84.99 | Strong Match |
| 50-69.99 | Moderate Match |
| 40-49.99 | Weak Match |
| Below 40 | Low Match |

## 7. Explainable Output

generate_candidate_score() returns:

- Candidate information
- Normalized component scores
- Percentage component scores
- Final ATS score
- Classification
- Role-specific weights
- Explanation
- Missing-data information

## 8. Day 14 Ranking Decision Logic

Day 14 consumes the ATS score produced by Day 13.

It does not recalculate the score.

Candidates are sorted by ATS score in descending order.

### Decision Thresholds

| Score | Decision |
|---:|---|
| >= 70 | SHORTLIST |
| 50-69.99 | REVIEW |
| < 50 | AUTO-REJECT |

## 9. Complete Flow

Candidate Data
|
v
Component Analysis
|
v
Normalize Components
|
v
Select Role Weights
|
v
Weighted Score
|
v
ATS Score
|
v
Day 13 Classification
|
v
Day 14 Ranking
|
v
Decision Zone
|
v
SHORTLIST / REVIEW / AUTO-REJECT

## 10. Source Files

ATS scoring:

src/ats_scoring/engine.py

Candidate ranking:

src/candidate_ranking/engine.py

Scoring tests:

tests/ats_tests/test_ats_scoring.py

Ranking tests:

tests/ranking_tests/test_candidate_ranking.py
