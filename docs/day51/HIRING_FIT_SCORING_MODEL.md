# Day 51: Hiring Fit Scoring Model

## Formula

Hiring Fit Score = Sum of (Stage Score x Normalized Stage Weight)

## Example: Data Analyst

ATS = 85
Screening = 80
HR Interview = 88
Technical Interview = 90
Machine Test = 92

Weights:

ATS = 0.10
Screening = 0.15
HR Interview = 0.15
Technical Interview = 0.30
Machine Test = 0.30

Calculation:

(85 x 0.10) +
(80 x 0.15) +
(88 x 0.15) +
(90 x 0.30) +
(92 x 0.30)

Hiring Fit Score = 88.00

## Performance categories

85-100: Excellent
70-84.99: Strong
55-69.99: Moderate
Below 55: Development Required

These categories are configurable research thresholds.

## Explainability

Every report includes:
- Raw stage score
- Original stage weight
- Normalized stage weight
- Weighted contribution
- Final Hiring Fit Score
- Missing-stage information
- Human review requirement

The score is not a probability of job success.
