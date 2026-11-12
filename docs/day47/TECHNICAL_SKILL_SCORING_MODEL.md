# Day 47 - Technical Skill Scoring Model

## Objective
Evaluate depth of technical knowledge beyond surface-level answers using an explainable, evidence-based rubric.

## Scoring parameters
Every answer is evaluated on a 0-100 scale for:
- Accuracy: explicit coverage of expected technical concepts.
- Depth: explanation length and elaboration signals such as examples, trade-offs, limitations and edge cases.
- Logical reasoning: sequencing, conditional reasoning and cause/effect signals.
- Real-world applicability: evidence of implementation, testing, deployment, monitoring, security or business use.

## Question-type rubric weights

| Question type | Accuracy | Depth | Logical reasoning | Applicability |
|---|---:|---:|---:|---:|
| Conceptual | 40% | 25% | 20% | 15% |
| Scenario | 25% | 20% | 30% | 25% |
| Coding | 35% | 20% | 25% | 20% |
| System design | 25% | 25% | 25% | 25% |
| Technical behavioral | 20% | 25% | 25% | 30% |

Weights sum to 100% for each question type.

## Difficulty normalization
Scores always remain on a common 0-100 scale. Difficulty changes the evidence threshold used by the depth heuristic:
- Beginner: 12-word depth reference and at least 1 expected concept.
- Intermediate: 25-word depth reference and at least 2 expected concepts.
- Advanced: 40-word depth reference and at least 3 expected concepts.

The accuracy score uses the supplied expected-concept list for that question. Interviewers should provide an appropriately comprehensive list for the question's difficulty.

## Shallow-answer detection
An answer is flagged as shallow when at least two of these conditions apply:
1. It is shorter than the difficulty-specific word reference.
2. It explicitly covers less than half of the expected concepts.
3. Its depth heuristic score is below 40/100.

A shallow flag is an indicator for human review, not an automatic rejection.

## Explainability
Each component returns a score, evidence list and explanation. The overall score is the sum of each component score multiplied by the selected question-type weight. Skill-level scores are the arithmetic mean of question scores for that skill.

## Deliverables
- Engine: `src/interview_system/technical_scoring_engine.py`
- Demonstration: `run_day47_scoring_demo.py`
- Tests: `tests/day47/test_technical_scoring_engine.py`
- JSON report: `outputs/day47/technical_skill_evaluation.json`
- Human-readable report: `outputs/day47/technical_skill_evaluation.md`

## Limitations and responsible use
This implementation uses transparent text heuristics, not semantic understanding. Keyword presence does not prove correctness, and word count or signal phrases do not prove deep reasoning. A qualified interviewer must review the answer, expected concepts and evidence, and may override the heuristic score with a documented reason. Do not use the automated score alone for hiring decisions.
