# Day 43 - AI Ethics Documentation

## Consent Requirements
Record whether consent was granted, the purpose of processing,
the consent timestamp, and the policy version.
A withdrawn consent record requires review.

## Fairness of Scoring
Scoring should use job-related evidence and consistent criteria.
Demographic attributes must not be used as scoring inputs.

## Demographic Signal Removal
Configured demographic fields are removed before candidate data
is passed to the scoring workflow.

## Explainability
Component scores, configured weights, and the final score are
recorded to make the calculation reviewable.

## Data Retention
The system checks whether records remain within a configurable
retention period or require deletion review.

## Human Oversight
Recruiters should review ambiguous results and potential disparities.

This document describes technical controls. It is not legal advice.
