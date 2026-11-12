from src.interview_system.malpractice_detection_engine import (
    MalpracticeDetectionEngine,
    InterviewIntegrityEvents
)


def run_demo():

    engine = MalpracticeDetectionEngine()

    candidate = InterviewIntegrityEvents(
        interview_id="DEMO-INT-049",
        duration_minutes=30,
        tab_switches=7,
        screen_focus_losses=6,
        external_voice_events=2,
        looking_away_events=9,
        repeated_event_intervals=4,
        consent_confirmed=True
    )

    report = engine.analyze(candidate)

    engine.save_report(
        report,
        "outputs/day49/integrity_detection_report.json"
    )

    print("\nDAY 49 DEMONSTRATION")
    print("=" * 45)

    print("Analysis:", report["analysis_status"])
    print("Pattern:", report["pattern_analysis"]["status"])
    print("Review tag:", report["risk_assessment"]["risk_tag"])
    print("Flags:", len(report["threshold_flags"]))
    print("Alerts:", len(report["alerts"]))
    print("Human review:", report["human_review"]["required"])
    print("Automatic rejection:", "DISABLED")

    print("\nDEMONSTRATION COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    run_demo()
