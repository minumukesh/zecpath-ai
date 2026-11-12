import json
from pathlib import Path

from src.answer_understanding import understand_answer


ROOT = Path(__file__).resolve().parent

DATA_DIR = ROOT / "data" / "day25_answer_understanding"
OUTPUT_DIR = ROOT / "outputs" / "day25"


TEST_CASES = [
    {
        "id": "ANS001",
        "type": "skills",
        "answer": "I have experience with Python, SQL and Power BI.",
    },
    {
        "id": "ANS002",
        "type": "experience",
        "answer": "I have 3 years of experience in data analysis.",
    },
    {
        "id": "ANS003",
        "type": "availability",
        "answer": "I am available immediately.",
    },
    {
        "id": "ANS004",
        "type": "salary",
        "answer": "My expected salary is 6 LPA.",
    },
    {
        "id": "ANS005",
        "type": "off_topic",
        "answer": "I watched a great movie yesterday.",
    },
    {
        "id": "ANS006",
        "type": "missing",
        "answer": "Not sure.",
    },
    {
        "id": "ANS007",
        "type": "combined",
        "answer": (
            "I have 2 years of experience with Python and SQL, "
            "and I can join immediately."
        ),
    },
    {
        "id": "ANS008",
        "type": "partial",
        "answer": "Python",
    },
]


def save_json(path, data):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


def main():

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = []

    print()
    print("=" * 70)
    print("DAY 25 - ANSWER INTENT & UNDERSTANDING ENGINE")
    print("=" * 70)

    for case in TEST_CASES:

        result = understand_answer(case["answer"])

        results.append({
            "test_case_id": case["id"],
            "expected_type": case["type"],
            "answer": case["answer"],
            "result": result,
        })

        print()
        print(f"Test Case: {case['id']}")
        print(f"Answer: {case['answer']}")
        print(f"Intent: {result['intent']}")
        print(f"Status: {result['answer_status']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Skills: {result['extracted']['skills']}")
        print(f"Experience: {result['extracted']['experience']}")
        print(f"Availability: {result['extracted']['availability']}")
        print(f"Salary: {result['extracted']['salary']}")

    save_json(
        OUTPUT_DIR / "day25_answer_understanding_results.json",
        results
    )

    schema = {
        "schema_name": "zecpath_structured_candidate_answer",
        "version": "1.0",
        "fields": {
            "answer_text": "string",
            "intent": "string",
            "answer_status": [
                "VALID",
                "PARTIAL",
                "MISSING_OR_VAGUE",
                "OFF_TOPIC",
            ],
            "confidence": "float between 0.0 and 1.0",
            "semantic_data": {
                "skills": "list of strings",
                "experience": "object",
                "availability": "object",
                "salary": "object",
            },
        },
    }

    save_json(
        DATA_DIR / "structured_answer_schema.json",
        schema
    )

    intent_mapping = {
        "SKILLS": "Candidate mentions skills or technologies.",
        "EXPERIENCE": "Candidate mentions work or experience details.",
        "AVAILABILITY": "Candidate mentions joining or availability.",
        "SALARY_EXPECTATION": "Candidate mentions salary expectations.",
        "OFF_TOPIC": "Candidate response appears unrelated to screening.",
        "MISSING_OR_VAGUE": "Candidate response is missing or insufficient.",
        "GENERAL": "General response without a specific detected intent.",
    }

    save_json(
        DATA_DIR / "intent_mapping.json",
        intent_mapping
    )

    report = {
        "day": 25,
        "title": "Answer Intent & Understanding Engine",
        "status": "COMPLETED",
        "sample_count": len(TEST_CASES),
        "capabilities": [
            "Intent classification",
            "Skills extraction",
            "Experience extraction",
            "Availability extraction",
            "Salary expectation extraction",
            "Off-topic detection",
            "Missing/vague answer detection",
            "Structured semantic answer generation",
        ],
        "generated_files": [
            "outputs/day25/day25_answer_understanding_results.json",
            "data/day25_answer_understanding/structured_answer_schema.json",
            "data/day25_answer_understanding/intent_mapping.json",
        ],
    }

    save_json(
        OUTPUT_DIR / "day25_answer_understanding_report.json",
        report
    )

    print()
    print("=" * 70)
    print("DAY 25 DEMO COMPLETED")
    print("=" * 70)
    print(f"Sample answers processed: {len(TEST_CASES)}")
    print("Intent classification: IMPLEMENTED")
    print("Skills extraction: IMPLEMENTED")
    print("Experience extraction: IMPLEMENTED")
    print("Availability extraction: IMPLEMENTED")
    print("Salary extraction: IMPLEMENTED")
    print("Off-topic detection: IMPLEMENTED")
    print("Missing/vague detection: IMPLEMENTED")
    print("Structured semantic objects: IMPLEMENTED")
    print()
    print("Generated files:")
    print("  outputs/day25/day25_answer_understanding_results.json")
    print("  outputs/day25/day25_answer_understanding_report.json")
    print("  data/day25_answer_understanding/structured_answer_schema.json")
    print("  data/day25_answer_understanding/intent_mapping.json")
    print("=" * 70)


if __name__ == "__main__":
    main()
