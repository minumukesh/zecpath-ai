# Day 49: Risk Flagging System Design

| Condition | Review tag | Action |
|---|---|---|
| No threshold exceeded | NO_THRESHOLD_FLAG | No event-based review flag |
| One or more thresholds exceeded | REVIEW_REQUIRED | Human review |
| Three or more thresholds exceeded | HIGH_REVIEW_PRIORITY | Prioritized human review |
| Consent missing | NOT_ASSESSED | Block assessment |

## Alert types

- Individual signal threshold alert
- Multiple-signal pattern alert
- Missing-consent alert

## Safeguards

- No automatic cheating verdict.
- No automatic candidate rejection.
- No candidate ranking based on event counts.
- Human reviewer must consider context.
- Technical errors and accessibility needs must be checked.
- Candidates should be able to challenge inaccurate records.
