from src.interview_system.behavioral_analysis_engine import (
    BehavioralAnalysisEngine,
    BehavioralObservation
)


def run_demo():

    engine = BehavioralAnalysisEngine()

    candidate = BehavioralObservation(
        observation_minutes=20,
        focus_observations=50,
        focused_observations=42,
        distraction_events=4,
        gaze_stability=0.72,
        head_movement_events=12,
        facial_engagement_observations=35,
        nervous_gesture_events=6
    )

    report = engine.analyze(candidate)

    output_path = (
        "outputs/day48/behavioral_analysis_report.json"
    )

    engine.save_report(report, output_path)

    print("\nDAY 48 BEHAVIORAL AI DEMONSTRATION")
    print("=" * 45)
    print("Analysis:", report["analysis_status"])
    print("Focus level:", report["task_focus"]["level"])
    print("Focus score:", report["task_focus"]["score"])
    print(
        "Distraction events/minute:",
        report["distraction_analysis"]["events_per_minute"]
    )
    print("Contextual signals recorded: 4")
    print("Automatic candidate ranking: Disabled")
    print("Human review required: Yes")
    print("Report:", output_path)
    print("\nDEMONSTRATION COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    run_demo()
