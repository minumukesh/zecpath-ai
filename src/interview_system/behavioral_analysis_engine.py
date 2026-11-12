"""
ZECPATH-AI Day 48
Behavioral AI Analysis Engine

This is a non-invasive, explainable research prototype.

Important:
- Does not identify emotions.
- Does not infer honesty, confidence, or personality.
- Does not rank candidates.
- Does not penalize nervous gestures, gaze patterns, or facial expressions.
- Produces descriptive observations and a limited task-focus indicator.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any
import json
from pathlib import Path


@dataclass
class BehavioralObservation:
    observation_minutes: float
    focus_observations: int
    focused_observations: int
    distraction_events: int
    gaze_stability: float
    head_movement_events: int
    facial_engagement_observations: int
    nervous_gesture_events: int


class BehavioralAnalysisEngine:

    def analyze(self, observation: BehavioralObservation) -> Dict[str, Any]:

        self._validate(observation)

        total = observation.focus_observations
        minutes = observation.observation_minutes

        # Task-focus indicator
        if total == 0:
            focus_level = None
            focus_score = None
        else:
            focus_score = round(
                (observation.focused_observations / total) * 100, 2
            )

            if focus_score >= 80:
                focus_level = "HIGH_TASK_FOCUS"
            elif focus_score >= 60:
                focus_level = "MODERATE_TASK_FOCUS"
            else:
                focus_level = "LOW_TASK_FOCUS"

        # Distraction frequency per observation minute
        distraction_frequency = round(
            observation.distraction_events / minutes, 2
        )

        # Descriptive signals only
        contextual_signals = {
            "gaze_stability": {
                "value": observation.gaze_stability,
                "interpretation": (
                    "Recorded as a visual observation only. "
                    "Not treated as a measure of confidence or honesty."
                )
            },
            "head_movement_events": {
                "value": observation.head_movement_events,
                "interpretation": (
                    "Movement frequency is contextual and may reflect "
                    "communication style or individual differences."
                )
            },
            "facial_engagement_observations": {
                "value": observation.facial_engagement_observations,
                "interpretation": (
                    "Recorded without emotion recognition or personality inference."
                )
            },
            "nervous_gesture_events": {
                "value": observation.nervous_gesture_events,
                "interpretation": (
                    "Recorded descriptively only. Never treated as a negative "
                    "candidate score."
                )
            }
        }

        result = {
            "project": "ZECPATH-AI",
            "day": 48,
            "module": "Behavioral AI Research and Design",
            "analysis_status": "COMPLETED",
            "observation_duration_minutes": minutes,
            "task_focus": {
                "score": focus_score,
                "level": focus_level,
                "focused_observations": observation.focused_observations,
                "total_observations": total,
                "meaning": (
                    "Descriptive task-related attention indicator, "
                    "not a measure of ability or suitability."
                )
            },
            "distraction_analysis": {
                "total_events": observation.distraction_events,
                "events_per_minute": distraction_frequency
            },
            "contextual_behavioral_signals": contextual_signals,
            "signal_to_insight_mapping": self._mapping(),
            "limitations": [
                "Behavioral observations do not reveal internal mental states.",
                "Gaze patterns vary across individuals and cultures.",
                "Head movement and facial behavior are context-dependent.",
                "Nervous gestures must not be treated as negative evidence.",
                "Accessibility and neurodiversity must be respected.",
                "Insufficient or missing observations must not be treated as poor performance."
            ],
            "decision_policy": {
                "automatic_candidate_ranking": False,
                "automatic_hiring_decision": False,
                "human_review_required": True,
                "consent_required": True
            }
        }

        return result

    @staticmethod
    def _validate(observation: BehavioralObservation):

        if observation.observation_minutes <= 0:
            raise ValueError("Observation duration must be greater than zero.")

        if observation.focus_observations < 0:
            raise ValueError("Focus observations cannot be negative.")

        if observation.focused_observations < 0:
            raise ValueError("Focused observations cannot be negative.")

        if observation.focused_observations > observation.focus_observations:
            raise ValueError(
                "Focused observations cannot exceed total observations."
            )

        count_fields = [
            observation.distraction_events,
            observation.head_movement_events,
            observation.facial_engagement_observations,
            observation.nervous_gesture_events
        ]

        if any(value < 0 for value in count_fields):
            raise ValueError("Event counts cannot be negative.")

        if not 0 <= observation.gaze_stability <= 1:
            raise ValueError("Gaze stability must be between 0 and 1.")

    @staticmethod
    def _mapping():

        return {
            "eye_movement_and_gaze": (
                "Contextual visual observation; no confidence or honesty score."
            ),
            "head_movement": (
                "Descriptive movement frequency; no personality inference."
            ),
            "facial_engagement": (
                "Visible engagement observations only; no emotion detection."
            ),
            "attention_patterns": (
                "Task-related focus observations may produce a descriptive focus indicator."
            ),
            "distraction_frequency": (
                "Number of observed distraction events per minute."
            ),
            "nervous_gestures": (
                "Recorded for context only; excluded from scoring."
            )
        }

    @staticmethod
    def save_report(report: Dict[str, Any], output_path: str):

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        return str(path)


def main():

    engine = BehavioralAnalysisEngine()

    sample = BehavioralObservation(
        observation_minutes=20,
        focus_observations=50,
        focused_observations=42,
        distraction_events=4,
        gaze_stability=0.72,
        head_movement_events=12,
        facial_engagement_observations=35,
        nervous_gesture_events=6
    )

    report = engine.analyze(sample)

    output = "outputs/day48/behavioral_analysis_report.json"
    engine.save_report(report, output)

    print("\nBEHAVIORAL ANALYSIS RESULT")
    print("=" * 45)
    print("Task focus:", report["task_focus"]["level"])
    print("Focus score:", report["task_focus"]["score"])
    print(
        "Distraction frequency:",
        report["distraction_analysis"]["events_per_minute"],
        "events/minute"
    )
    print("Nervous gestures:", sample.nervous_gesture_events)
    print("Nervous gestures are NOT penalized.")
    print("Automatic hiring decision:", "DISABLED")
    print("Report saved:", output)


if __name__ == "__main__":
    main()
