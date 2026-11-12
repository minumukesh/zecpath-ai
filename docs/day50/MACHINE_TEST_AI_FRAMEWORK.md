# ZECPATH-AI Day 50
# Machine Test AI Framework

## 1. Objective

Design a task-based evaluation system that measures practical technical
skills through structured machine tests.

## 2. Supported Task Types

### Coding Problems
Candidates solve programming problems. Evaluation considers test-case
correctness, efficiency, code quality, and problem-solving approach.

### Debugging Tasks
Candidates identify and correct defects in existing code. Evaluation
considers whether the defect is resolved and whether the solution
addresses the root cause.

### File-Based Tasks
Candidates process structured files such as CSV or JSON. Evaluation
considers data correctness, validation, handling, and output quality.

### Mini System Design
Candidates design a small technical system. Evaluation considers
architecture, component separation, reliability, scalability, and
design trade-offs.

## 3. Evaluation Metrics

| Metric | Weight | Description |
|---|---:|---|
| Correctness | 40% | Passed tests or rubric checks |
| Efficiency | 20% | Execution/resource efficiency |
| Code quality | 20% | Readability, structure, maintainability |
| Problem-solving | 20% | Reasoning and approach |

## 4. Time-Based Scoring

A configurable penalty is applied when the candidate exceeds the
task time limit.

The prototype uses a penalty of two points per excess minute,
capped at twenty points.

This is a configurable research assumption and must be validated
before production use.

## 5. Input and Output Capture

The framework records:
- Candidate ID
- Task ID and task type
- Code or design snapshot
- Execution output
- Passed and total test cases
- Evaluation metrics
- Time limit and time taken

## 6. Scoring Workflow

Task assignment
      |
      v
Candidate submission
      |
      v
Snapshot and execution evidence capture
      |
      v
Correctness evaluation
      |
      v
Efficiency and code quality evaluation
      |
      v
Problem-solving rubric evaluation
      |
      v
Time adjustment
      |
      v
Explainable evaluation report

## 7. Explainability

Every metric has:
- A numerical score
- A configured weight
- A weighted contribution
- A short explanation

The final report includes the base score, time penalty, final score,
performance category, and improvement suggestions.

## 8. Security Considerations

The prototype evaluates supplied execution evidence. It does not
execute untrusted code.

A production machine-test platform must execute candidate submissions
inside isolated environments with CPU, memory, network, filesystem,
and execution-time restrictions.

## 9. Limitations

Efficiency, code quality, and problem-solving scores require validated
evaluation mechanisms. The demo uses sample evaluator scores and
synthetic execution evidence.

## 10. Deliverables

- Machine test AI framework
- Task evaluation logic
- Scoring model
- Input/output capture structure
- Unit tests
- Demonstration
- JSON and Markdown reports
