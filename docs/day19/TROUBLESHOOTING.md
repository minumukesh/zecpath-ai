# Zecpath AI ATS Troubleshooting Guide

## 1. Full Test Suite

Run:

python -m pytest -v

Verified project result:

70 passed, 1 warning

If a test fails, inspect the first failing test before modifying code.

## 2. Invalid File Type

Run:

python -m pytest -v tests/api_tests/test_ats_api.py::TestATSAPI::test_invalid_file_type

Unsupported resume file types should return:

415 Unsupported Media Type

Implementation:

src/ats_api/api.py

## 3. Resume Not Found

If the API returns:

RESUME_NOT_FOUND

check whether the resume ID exists in the API resume store.

Upload the resume before attempting parse or score operations.

## 4. Job Not Found

If scoring returns:

JOB_NOT_FOUND

check the requested job ID.

The current API contains:

JOB-001

## 5. Unexpected ATS Score

Check:

- Skill Match
- Experience Relevance
- Education Alignment
- Semantic Similarity

Then verify the selected role.

Implementation:

src/ats_scoring/engine.py

## 6. Unexpected Candidate Decision

Day 13 classification and Day 14 decision are different stages.

Flow:

ATS Score
|
v
Day 13 Classification
|
v
Day 14 Decision

Day 14 thresholds:

>= 70       SHORTLIST
50-69.99    REVIEW
< 50        AUTO-REJECT

## 7. Day 17 Mismatch

Day 17 compares AI decisions with manually expected decisions.

Mismatch cases should be recorded instead of silently changing expected
values.

Report:

outputs/day17/day17_ats_testing_report.json

## 8. Optimization Issues

Day 18 files:

src/ats_optimization/optimizer.py
src/ats_optimization/optimized_pipeline.py
run_day18_optimization.py

Run:

python -m pytest -v tests/optimization_tests/test_ats_optimization.py

## 9. Performance Investigation

Day 18 generated:

outputs/day18/day18_performance_report.json

Use the benchmark report when investigating performance changes.

## 10. Import Errors

If Python reports:

ModuleNotFoundError

check:

1. The command is being run from the project root.
2. The virtual environment is activated.
3. The referenced module exists.
4. Required package files are present.

## 11. Safe Debugging Rule

Before changing an existing ATS component:

1. Run the relevant test.
2. Identify the failing component.
3. Inspect the implementation.
4. Make the smallest necessary change.
5. Run the targeted test.
6. Run the complete test suite.

Avoid creating duplicate scoring, ranking, or pipeline implementations.
