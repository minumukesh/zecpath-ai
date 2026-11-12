# Day 40 - HR Interview Simulation

## Objective

Test a simulated HR interview evaluation workflow using multiple candidate
profiles and compare the generated scores with supplied manual references.

## Workflow

Candidate Simulation Cases
          |
          v
Calculate Weighted Interview Score
          |
          v
Assign Performance Label
          |
          v
Compare AI Score and Label with Manual Reference
          |
          v
Identify Score and Decision Differences
          |
          v
Calculate Evaluation Metrics
          |
          v
Generate Test Report and Recommendations

## Candidate Types

- Confident
- Hesitant
- Inexperienced
- Overqualified

These are scenario labels. The system should not automatically penalize
hesitation, limited experience, or overqualification.

## Scoring Parameters

- Answer relevance: 35%
- Communication: 20%
- Problem-solving: 25%
- Consistency: 20%

The final score is calculated as a weighted average from 0 to 100.

## Comparison

The system compares each calculated score and performance label with the
manual reference supplied in the dataset. The default score tolerance is
10 points.

## Metrics

- Score consistency rate
- Decision accuracy against supplied manual labels
- Overall consistency rate
- Number of inconsistencies

These metrics describe the supplied test cases only. They do not establish
real-world model accuracy.

## Run

    python .\run_day40_hr_interview_simulation.py

## Run Day 40 Tests

    python -m pytest -v .\tests\hr_interview_simulation_tests\test_hr_interview_simulation.py

## Outputs

Generated reports are stored in `outputs/day40/`.

## Limitations

The current implementation uses manually supplied simulation scores and
reference decisions. It does not run a live AI interview or independently
validate the correctness of human judgments. Human review is required
before using the system in a real hiring process.
