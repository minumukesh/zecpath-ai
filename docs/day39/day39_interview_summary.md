# Day 39 - Interview Summary Generator

## Objective

Convert supplied AI and HR interview analysis into a structured,
recruiter-friendly summary.

## Workflow

Interview Responses and Evaluation Scores
                 |
                 v
        Collect Interview Data
                 |
                 v
       Organize Strengths and
       Weaknesses / Development Areas
                 |
                 v
       Review Collaboration Indicators
                 |
                 v
       Identify Risk Flags and
       Possible Inconsistencies
                 |
                 v
       Calculate Overall Performance
                 |
                 v
       Generate Structured Summary
                 |
                 v
       Export JSON and Markdown Reports

## Main Features

1. Structures candidate strengths and development areas.
2. Records job-related collaboration indicators.
3. Displays supplied risk flags for human review.
4. detects possible differences between answers on the same topic.
5. Calculates the average of available interview scores.
6. Records missing information.
7. Generates a natural-language summary.
8. Exports JSON and Markdown reports.

## Report Structure

- Candidate details
- Strengths
- Weaknesses / development areas
- Collaboration indicators
- Risk flags
- Possible inconsistencies
- Overall interview performance
- Missing information
- Natural-language summary
- Human review notice

## Run the Demo

    python .\run_day39_interview_summary.py

## Run Day 39 Tests

    python -m pytest -v .\tests\interview_summary_tests\test_interview_summary.py

## Outputs

Generated reports are stored in `outputs/day39/`.

## Important Limitations

The system organizes supplied information and uses simple rules to flag
possible inconsistencies. Different answers do not prove dishonesty.
Collaboration indicators must be job-related. Human review is required,
and this report must not be used as the sole basis for hiring decisions.
