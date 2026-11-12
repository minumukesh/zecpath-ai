# Day 50: Machine Test Scoring Model

## Metric weights

| Metric | Weight |
|---|---:|
| Correctness | 0.40 |
| Efficiency | 0.20 |
| Code quality | 0.20 |
| Problem-solving | 0.20 |

## Base score

Base score =
(Correctness x 0.40) +
(Efficiency x 0.20) +
(Code Quality x 0.20) +
(Problem-solving x 0.20)

## Time penalty

If time taken exceeds the limit:

Time penalty = min(excess minutes x 2, 20)

Otherwise, the time penalty is zero.

## Final score

Final score = max(0, Base score - Time penalty)

## Performance categories

| Final score | Category |
|---|---|
| 85-100 | Excellent |
| 70-84.99 | Good |
| 50-69.99 | Average |
| Below 50 | Needs Improvement |

These are initial configurable research thresholds, not validated
industry benchmarks.
