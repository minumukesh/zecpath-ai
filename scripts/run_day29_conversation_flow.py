import json
from pathlib import Path

from src.conversation_flow import (
    ConversationEngine,
    ConversationConfig,
    run_sample_conversation,
)


OUTPUT_DIR = Path("outputs/day29")
SCENARIO_FILE = Path("data/day29_conversation_flow/scenarios.json")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 68)
    print("DAY 29 - AI CONVERSATION FLOW DESIGN")
    print("=" * 68)

    scenario_data = json.loads(
        SCENARIO_FILE.read_text(encoding="utf-8-sig")
    )

    print(f"Configured scenarios: {len(scenario_data['scenarios'])}")
    print()

    for scenario in scenario_data["scenarios"]:
        print(
            f"{scenario['scenario_id']}: "
            f"{scenario['description']}"
        )

    sample = run_sample_conversation()

    conversation_path = OUTPUT_DIR / "day29_sample_conversation.json"
    conversation_path.write_text(
        json.dumps(sample, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    engine = ConversationEngine(
        config=ConversationConfig(
            max_silence_retries=2,
            max_confusion_retries=2,
            max_repeated_answers=1,
            max_system_retries=2,
        )
    )

    # Demonstrate silence handling.
    engine.start()
    silence_result = engine.handle_silence()

    # Demonstrate system failure and retry logic.
    failure_engine = ConversationEngine()
    failure_engine.start()
    failure_result = failure_engine.handle_system_failure(
        "sample temporary failure"
    )

    demo_result = {
        "day": 29,
        "title": "AI Conversation Flow Design",
        "scenarios_loaded": len(scenario_data["scenarios"]),
        "sample_conversation": sample,
        "silence_handling": silence_result.to_dict(),
        "system_failure_handling": failure_result.to_dict(),
        "features": {
            "conversation_decision_tree": "IMPLEMENTED",
            "conversation_state_machine": "IMPLEMENTED",
            "silence_handling": "IMPLEMENTED",
            "confusion_handling": "IMPLEMENTED",
            "repeated_answer_handling": "IMPLEMENTED",
            "fallback_questions": "IMPLEMENTED",
            "follow_up_triggers": "IMPLEMENTED",
            "polite_failure_and_retry_logic": "IMPLEMENTED",
        },
    }

    report_path = OUTPUT_DIR / "day29_conversation_flow_report.json"
    report_path.write_text(
        json.dumps(demo_result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print()
    print("-" * 68)
    print("FEATURE STATUS")
    print("-" * 68)

    for name, status in demo_result["features"].items():
        print(f"{name}: {status}")

    print()
    print(f"Sample conversation: {conversation_path}")
    print(f"Conversation flow report: {report_path}")
    print()
    print("DAY 29 DEMO COMPLETED")
    print("=" * 68)


if __name__ == "__main__":
    main()
