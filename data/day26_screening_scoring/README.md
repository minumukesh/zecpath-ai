# Day 26 - Screening Scoring Engine

Objective:
Objectively evaluate candidate screening responses.

Scoring parameters:
- Clarity: 25%
- Relevance: 35%
- Completeness: 25%
- Consistency: 15%

The engine calculates a score for each question, normalizes
scores to a 0-100 scale, aggregates the overall screening score,
and returns explainable scoring output.

Important:
This first version uses transparent heuristics and keyword
coverage. It does not use a trained semantic model, and its
scores should support human review rather than replace it.
