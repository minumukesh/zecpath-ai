# Day 37 - HR Interview Scoring Engine

## Objective

Combine interview answer relevance, communication, confidence signals, and
consistency into a structured score.

## Workflow

Candidate Interview Responses
             |
             v
Score Each Answer for Relevance
             |
             v
Normalize Question Scores to 0-100
             |
             v
Collect Communication, Confidence, and Consistency Scores
             |
             v
Apply Configurable Weights
             |
             v
Calculate Final HR Interview Score
             |
             v
Generate Score Breakdown and Report

## Default Weights

- Answer relevance: 40%
- Communication: 25%
- Confidence: 20%
- Consistency: 15%

Weights can be configured. The engine normalizes configured weights so
their total equals 100%.

## Formula

Final Score =
(Relevance × 0.40) +
(Communication × 0.25) +
(Confidence × 0.20) +
(Consistency × 0.15)

All component scores are on a 0-100 scale.

## Score Bands

- 85-100: HIGH_SCORE
- 70-84.99: GOOD_SCORE
- 50-69.99: MODERATE_SCORE
- Below 50: LOW_SCORE

These labels describe prototype score ranges. They are not automatic
hiring decisions.

## Output

The engine produces:
- Candidate and role details
- Number of interview questions
- Individual component scores
- Configured weights
- Weighted contribution of each component
- Final score and score band
- Explanations and limitations
- JSON and Markdown reports

## Important Limitations

This is a prototype scoring framework. Its results depend on the quality
of the component scores supplied to it. Confidence scores should not be
treated as objective measurements of a person's personality or ability.
Recruiters should review the underlying interview evidence before making
decisions.
