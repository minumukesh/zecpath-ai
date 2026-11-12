# Day 34 - Dynamic Follow-Up Logic

## Objective
Enable adaptive questioning based on candidate responses.

## Workflow

Candidate Answer
        |
        v
Normalize Answer
        |
        v
Detect Answer Type
        |
        +---- Missing / Vague ----> Clarification Question
        |
        +---- Brief -------------> Request an Example
        |
        +---- Detailed ----------> Deeper or Scenario-Based Question
        |
        v
Check Previously Used Follow-Ups
        |
        +---- New Question ------> Ask Follow-Up
        |
        +---- All Used ----------> Recommend Human Review
        |
        v
Update Conversation State
        |
        v
Save Interview History

## Follow-up triggers

- Clarification: answer is missing, vague, or too brief.
- Example request: candidate needs to explain with a practical example.
- Deepening: ask what was learned or what happened next.
- Scenario follow-up: explore how the candidate would handle a related situation.
- Human review: no unused follow-up question is available.

## Conversation state

Each conversation tracks:

- Interview ID
- Candidate ID
- Job role
- Current state
- Turn count
- Previously used follow-up questions
- Question and answer history
- Follow-up trigger
- Timestamp

## Repetition prevention

The engine records follow-up prompts already used in the current interview.
It avoids selecting the same prompt again. If no unused prompt is available,
it recommends human review.

## Limitations

This is a rule-based prototype. Answer length and wording are only simple
signals. They do not prove confidence, honesty, answer quality, or job suitability.
