# Day 48: Signal-to-Score Mapping Model

| Observable signal | Measurable indicator | Scoring treatment |
|---|---|---|
| Task-related attention | Focused observation ratio | Descriptive focus indicator |
| Distraction | Events per minute | Descriptive frequency |
| Gaze stability | Normalized observation | Context only, no score |
| Head movement | Movement event count | Context only, no score |
| Facial engagement | Observation count | Context only, no score |
| Nervous gestures | Gesture event count | Context only, no penalty |

## Formula

Task focus indicator:
(Focused observations / Total focus observations) * 100

Distraction frequency:
Distraction events / Observation duration in minutes

## Important safeguards

- Nervous gestures do not reduce a score.
- Gaze stability is not a confidence or honesty measure.
- Facial expressions are not used for emotion detection.
- No candidate ranking is produced.
- Missing data is not interpreted as poor behavior.
- Human review and informed consent are required.
