# Day 65 - Scoring and Output Quality

## 1. ATS Scoring Consistency

The documented ATS scoring engine uses:
- Skill Match.
- Experience Relevance.
- Education Alignment.
- Semantic Similarity.

Role-based scoring weights must remain consistent with the existing ATS implementation.

## 2. Scoring Validation

- [ ] Verify all component scores use the expected scale.
- [ ] Verify component weights are normalized.
- [ ] Verify missing values are handled safely.
- [ ] Verify final scores remain within 0-100.
- [ ] Verify identical inputs produce consistent results.
- [ ] Verify ranking follows the ATS score.
- [ ] Test different job roles.

## 3. Candidate Ranking Consistency

Documented ranking thresholds:

| ATS Score | Decision |
|---|---|
| 70 or above | SHORTLIST |
| 50 to below 70 | REVIEW |
| Below 50 | AUTO-REJECT |

Verify that ranking does not independently recalculate the ATS score.

## 4. Output Readability

Recommended recruiter-facing output structure:

1. Candidate Information
2. Job Information
3. Overall ATS Score
4. Match Classification
5. Matching Skills
6. Missing Skills
7. Experience Evaluation
8. Education Evaluation
9. Semantic Matching Summary
10. Recommendation and Explanation

## 5. Report Quality

Reports should:
- Use consistent headings.
- Avoid duplicate information.
- Display numerical results clearly.
- Explain evaluation outcomes.
- Distinguish missing data from negative results.
- Include appropriate human-review notices.

## 6. Quality Tests

- [ ] Same input produces consistent score.
- [ ] Missing skills do not crash scoring.
- [ ] Empty candidate profiles are handled.
- [ ] Invalid score values are rejected or normalized safely.
- [ ] Ranking thresholds are respected.
- [ ] Report fields are readable and complete.

## 7. Conclusion

These checks define the expected quality of ATS scoring, candidate ranking and recruiter-facing outputs.
