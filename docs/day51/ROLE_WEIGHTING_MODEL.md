# Day 51: Role-Specific Weighting Model

## Data Analyst

ATS: 10%
Screening: 15%
HR Interview: 15%
Technical Interview: 30%
Machine Test: 30%

## Data Scientist

ATS: 10%
Screening: 10%
HR Interview: 10%
Technical Interview: 35%
Machine Test: 35%

## Software Developer

ATS: 10%
Screening: 10%
HR Interview: 10%
Technical Interview: 30%
Machine Test: 40%

## Business Analyst

ATS: 10%
Screening: 20%
HR Interview: 20%
Technical Interview: 25%
Machine Test: 25%

## General

All five stages: 20% each.

## Weight validation

All role weights must:
- Include all five stages.
- Be non-negative.
- Sum to 1.0.

## Missing-stage normalization

When a stage score is unavailable, the remaining stage weights
are normalized to sum to 1.0.

The missing score is not treated as zero.

## Validation requirement

Weights are research defaults and must be validated against
job requirements and recruitment outcomes before production use.
