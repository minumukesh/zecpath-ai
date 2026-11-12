# Day 49: Malpractice Detection Logic

## Signals and default review thresholds

| Signal | Threshold |
|---|---:|
| Tab switches | 5 |
| Screen focus losses | 5 |
| External voice events | 3 |
| Looking-away events | 8 |
| Repeated event intervals | 3 |

These values are configurable research defaults, not scientifically
validated cheating thresholds.

## Pattern recognition

1. Validate the interview event record.
2. Compare each event count against its threshold.
3. Generate an individual flag for each exceeded threshold.
4. Identify whether multiple signal categories were flagged.
5. Generate review alerts.
6. Require human interpretation.

## Important distinction

The system detects unusual event patterns, not cheating itself.

A candidate must never be declared dishonest solely because a threshold
was exceeded.
