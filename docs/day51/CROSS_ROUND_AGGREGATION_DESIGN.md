# ZECPATH-AI Day 51
# Cross-Round Aggregation Engine

## 1. Objective

Combine five recruitment evaluation stages into a unified Hiring Fit Score.

The five stages are:

1. ATS
2. Screening
3. HR Interview
4. Technical Interview
5. Machine Test

## 2. Role-Specific Weighting

| Stage | Data Analyst | Data Scientist | Developer | Business Analyst |
|---|---:|---:|---:|---:|
| ATS | 10% | 10% | 10% | 10% |
| Screening | 15% | 10% | 10% | 20% |
| HR Interview | 15% | 10% | 10% | 20% |
| Technical Interview | 30% | 35% | 30% | 25% |
| Machine Test | 30% | 35% | 40% | 25% |

These are configurable initial design weights. They should be validated
against job analysis and real evaluation outcomes before production use.

## 3. Hiring Fit Score

Hiring Fit Score is the weighted average of available stage scores.

Each score is normalized to a common 0-100 scale before aggregation.

## 4. Missing Stage Handling

A missing stage is excluded from the calculation.

The remaining available weights are normalized to sum to one.

Missing stages are not automatically assigned zero.

Reports clearly identify which stages are missing.

## 5. Profile Normalization

The prototype supports profile groups:

- Standard
- Experienced
- Entry level
- Career transition

No arbitrary bonus or penalty is applied to a candidate based on
their profile group.

All candidates use the same job-relevant scoring method.

## 6. Transparency

The unified candidate score object contains:

- Candidate information
- Target role
- Stage scores
- Original role weights
- Normalized weights
- Weighted contributions
- Hiring Fit Score
- Performance category
- Missing-stage warnings
- Explanation of the result

## 7. Architecture

ATS Score ---------+
Screening Score ---+
HR Interview ------+
Technical Score ---+--> Cross-Round Aggregation Engine
Machine Test ------+             |
                                  v
                         Role Weight Selection
                                  |
                                  v
                         Score Normalization
                                  |
                                  v
                         Weighted Aggregation
                                  |
                                  v
                         Hiring Fit Calculator
                                  |
                                  v
                         Unified Candidate Object
                                  |
                                  v
                         Explainable Report

## 8. Decision Policy

The Hiring Fit Score is a decision-support indicator.

It is not a probability of job success.

It must not be used as the sole basis for hiring or rejection.
Human review is required.

## 9. Limitations

This prototype accepts stage scores through a unified input object.
It does not yet automatically retrieve results from every previous
module's storage or database.

Production integration requires verified adapters for each stage,
consistent score definitions, and validated role-specific weights.

## 10. Deliverables

- Hiring Fit Calculator
- Cross-Round Aggregation Engine
- Unified Candidate Score Object
- Role-specific weight system
- Score normalization
- Explainable evaluation reports
- Unit tests and demonstration
