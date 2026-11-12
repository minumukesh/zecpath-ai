"""
ZECPATH-AI Day 49
Malpractice and Integrity Detection Engine

This is an explainable event-based research prototype.

It identifies unusual interview-session events for human review.
It does not prove cheating, identify external speakers, or make
automatic candidate rejection decisions.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, List
from pathlib import Path
from collections import Counter
import json


@dataclass
class InterviewIntegrityEvents:

    interview_id: str

    duration_minutes: float

    tab_switches: int = 0

    screen_focus_losses: int = 0

    external_voice_events: int = 0

    looking_away_events: int = 0

    repeated_event_intervals: int = 0

    consent_confirmed: bool = False


class MalpracticeDetectionEngine:

    def __init__(self):

        # Thresholds are configurable research defaults.
        self.thresholds = {
            "tab_switches": 5,
            "screen_focus_losses": 5,
            "external_voice_events": 3,
            "looking_away_events": 8,
            "repeated_event_intervals": 3
        }

        self.weights = {
            "tab_switches": 2,
            "screen_focus_losses": 2,
            "external_voice_events": 2,
            "looking_away_events": 1,
            "repeated_event_intervals": 2
        }

    def analyze(self, events: InterviewIntegrityEvents) -> Dict[str, Any]:

        self._validate(events)

        observations = {
            "tab_switches": events.tab_switches,
            "screen_focus_losses": events.screen_focus_losses,
            "external_voice_events": events.external_voice_events,
            "looking_away_events": events.looking_away_events,
            "repeated_event_intervals": events.repeated_event_intervals
        }

        flags = []
        alerts = []

        for signal, value in observations.items():

            threshold = self.thresholds[signal]

            if value >= threshold:

                flags.append({
                    "signal": signal,
                    "observed_value": value,
                    "threshold": threshold,
                    "status": "THRESHOLD_EXCEEDED",
                    "explanation": self._explanation(signal)
                })

                alerts.append({
                    "alert_type": signal.upper(),
                    "message": (
                        f"{signal.replace('_', ' ').title()} "
                        f"reached {value}; review threshold is {threshold}."
                    ),
                    "severity": "REVIEW_REQUIRED"
                })

        # Pattern recognition:
        # A pattern is flagged only when multiple different signal
        # categories exceed their thresholds.
        exceeded_signals = [flag["signal"] for flag in flags]

        if len(exceeded_signals) >= 2:
            pattern_status = "MULTI_SIGNAL_PATTERN_DETECTED"

            alerts.append({
                "alert_type": "MULTI_SIGNAL_PATTERN",
                "message": (
                    "Multiple event categories exceeded their review "
                    "thresholds. A human reviewer should examine the context."
                ),
                "severity": "REVIEW_REQUIRED"
            })

        elif len(exceeded_signals) == 1:
            pattern_status = "SINGLE_SIGNAL_PATTERN"

        else:
            pattern_status = "NO_THRESHOLD_PATTERN"

        # Transparent research indicator.
        # It is NOT a probability of cheating.
        raw_score = sum(
            min(observations[name], self.thresholds[name] * 2)
            * self.weights[name]
            / max(self.thresholds[name] * 2, 1)
            for name in observations
        )

        maximum_score = sum(self.weights.values())

        risk_indicator = round(
            (raw_score / maximum_score) * 100, 2
        )

        # Risk tags indicate review priority only.
        if len(exceeded_signals) >= 3:
            risk_tag = "HIGH_REVIEW_PRIORITY"

        elif len(exceeded_signals) >= 1:
            risk_tag = "REVIEW_REQUIRED"

        else:
            risk_tag = "NO_THRESHOLD_FLAG"

        if not events.consent_confirmed:
            alerts.append({
                "alert_type": "CONSENT_MISSING",
                "message": (
                    "Monitoring data must not be collected or processed "
                    "without appropriate informed consent."
                ),
                "severity": "DATA_COLLECTION_BLOCKED"
            })

        # When consent is missing, no behavioral/integrity conclusion
        # should be produced from the supplied observations.
        if not events.consent_confirmed:
            risk_tag = "NOT_ASSESSED"
            risk_indicator = None
            flags = []
            pattern_status = "NOT_ASSESSED"

        return {
            "project": "ZECPATH-AI",
            "day": 49,
            "module": "Malpractice and Integrity Detection",
            "interview_id": events.interview_id,
            "analysis_status": (
                "COMPLETED" if events.consent_confirmed
                else "BLOCKED_CONSENT_REQUIRED"
            ),
            "observation_duration_minutes": events.duration_minutes,

            "observed_events": observations,

            "threshold_flags": flags,

            "pattern_analysis": {
                "status": pattern_status,
                "exceeded_signal_count": len(exceeded_signals),
                "exceeded_signals": exceeded_signals
            },

            "risk_assessment": {
                "review_indicator": risk_indicator,
                "risk_tag": risk_tag,
                "meaning": (
                    "A configurable review-priority indicator, not a "
                    "probability of malpractice or proof of cheating."
                )
            },

            "alerts": alerts,

            "human_review": {
                "required": True,
                "automatic_candidate_rejection": False,
                "automatic_cheating_verdict": False,
                "reviewer_must_check_context": True
            },

            "limitations": [
                "Tab switching may occur for legitimate reasons.",
                "Screen focus loss does not prove external assistance.",
                "External voice events do not identify the speaker.",
                "Looking away is not evidence of dishonesty.",
                "Technical failures can create false alerts.",
                "Accessibility needs and assistive technologies must be considered.",
                "Thresholds require validation before real-world use."
            ]
        }

    @staticmethod
    def _explanation(signal):

        explanations = {
            "tab_switches": (
                "Repeated tab changes were observed. They may have "
                "legitimate explanations and require context review."
            ),
            "screen_focus_losses": (
                "The interview window lost focus repeatedly. This does "
                "not establish that another application was used improperly."
            ),
            "external_voice_events": (
                "Background voice events were recorded. The system does "
                "not identify speakers or determine whether assistance occurred."
            ),
            "looking_away_events": (
                "Looking-away events were recorded descriptively. "
                "Gaze behavior is not evidence of cheating."
            ),
            "repeated_event_intervals": (
                "Repeated event timing was detected and should be "
                "reviewed alongside the interview context."
            )
        }

        return explanations[signal]

    @staticmethod
    def _validate(events):

        if not events.interview_id.strip():
            raise ValueError("Interview ID cannot be empty.")

        if events.duration_minutes <= 0:
            raise ValueError(
                "Interview duration must be greater than zero."
            )

        values = [
            events.tab_switches,
            events.screen_focus_losses,
            events.external_voice_events,
            events.looking_away_events,
            events.repeated_event_intervals
        ]

        if any(not isinstance(value, int) or value < 0 for value in values):
            raise ValueError(
                "Event counts must be non-negative integers."
            )

    @staticmethod
    def save_report(report, output_path):

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        return str(path)


def main():

    engine = MalpracticeDetectionEngine()

    sample = InterviewIntegrityEvents(
        interview_id="DEMO-INT-049",
        duration_minutes=30,
        tab_switches=7,
        screen_focus_losses=6,
        external_voice_events=2,
        looking_away_events=9,
        repeated_event_intervals=4,
        consent_confirmed=True
    )

    report = engine.analyze(sample)

    output = "outputs/day49/integrity_detection_report.json"

    engine.save_report(report, output)

    print("\nMALPRACTICE & INTEGRITY ANALYSIS")
    print("=" * 48)

    print("Interview ID:", report["interview_id"])
    print("Analysis:", report["analysis_status"])
    print("Pattern:", report["pattern_analysis"]["status"])
    print("Risk tag:", report["risk_assessment"]["risk_tag"])
    print(
        "Review indicator:",
        report["risk_assessment"]["review_indicator"]
    )
    print("Threshold flags:", len(report["threshold_flags"]))
    print("Alerts:", len(report["alerts"]))
    print("Human review required:", report["human_review"]["required"])
    print("Automatic rejection:", "DISABLED")

    print("\nReport saved:", output)


if __name__ == "__main__":
    main()
