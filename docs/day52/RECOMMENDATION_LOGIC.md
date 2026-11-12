# Day 52: Recommendation Logic

## Decision priority

1. Validate input data.
2. Calculate evidence completeness.
3. Review integrity alerts.
4. Check essential technical requirements.
5. Evaluate the Hiring Fit Score.
6. Generate a recommendation.
7. Explain the reasons.
8. Require human approval.

## Rules

SELECTED:
- Score is at least 80.
- Evidence is verified.
- All required stages are available.
- No unresolved integrity alerts exist.
- Decision confidence is at least 75.

HOLD / REVIEW:
- Integrity alerts are unresolved.
- A confirmed integrity issue requires review.
- Evidence is incomplete or unverified.
- Score is between 55 and 79.99.
- Confidence is below 75.

REJECTED:
- Score is below 55, or a documented essential technical
  requirement is not met, subject to human review.

## Hybrid approach

The engine combines numerical scores with explicit decision rules.
Rules can override a high numerical score when evidence requires review.

No automated hiring action is performed.
