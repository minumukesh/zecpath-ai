# Day 67 - Stakeholder Q&A Preparation

## 1. Project Overview

### Q1. What is Zecpath AI?

Zecpath AI is an AI-powered recruitment platform designed to support candidate analysis and organize different stages of the hiring workflow.

### Q2. What problem does it solve?

Traditional recruitment involves repetitive resume reviews, candidate comparisons and evaluation activities. Zecpath AI aims to organize these activities through specialized AI modules.

### Q3. Who are the intended users?

The intended users include candidates, recruiters and hiring teams.

## 2. AI and Technical Questions

### Q4. How does resume parsing work?

Resume parsing extracts information such as candidate details, education, experience and skills from resume documents.

### Q5. What is skill extraction?

Skill extraction identifies technical and professional skills from candidate information and organizes them into structured data.

### Q6. What is semantic matching?

Semantic matching compares the meaning and context of candidate qualifications with job requirements instead of relying only on exact keyword matches.

### Q7. What are the ATS scoring components?

The documented components are:

- Skill Match.
- Experience Relevance.
- Education Alignment.
- Semantic Similarity.

### Q8. What is the difference between scoring and ranking?

Scoring calculates an evaluation value for a candidate. Ranking orders candidates based on their scores.

### Q9. How does the system handle missing information?

Missing information should be handled through validation and controlled processing. It should not automatically be treated as proof that a candidate lacks a qualification.

### Q10. Why is human review important?

AI results can contain errors or incomplete information. Recruiters should review relevant evidence before making final hiring decisions.

## 3. Architecture Questions

### Q11. How do the modules communicate?

The planned architecture uses backend APIs to coordinate processing between application services, AI modules and data storage.

### Q12. Why use modular architecture?

Modular architecture separates responsibilities, making components easier to maintain, test and improve.

### Q13. How is candidate information stored?

The architecture includes database storage for structured candidate and recruitment information. The actual database implementation should be demonstrated using the current project.

## 4. Dataset and Testing Questions

### Q14. What data is used for the demonstration?

The Day 63 dataset contains 10 fictional candidates and 3 job descriptions, together with simulated ATS results, screening outputs and interview responses.

### Q15. Are the displayed ATS scores real model predictions?

No. The Day 63 ATS scores are simulated demonstration results. They should not be represented as production model predictions.

### Q16. How would you validate model accuracy?

Use manually labeled evaluation data, compare predictions with reference results and measure suitable metrics such as precision, recall and F1-score.

## 5. Business Questions

### Q17. What are the expected business benefits?

Potential benefits include reducing repetitive manual review, organizing candidate information and improving recruitment workflow visibility.

### Q18. Does the system replace recruiters?

No. It is intended to support recruitment activities. Human judgment and final hiring approval remain important.

### Q19. What are the future enhancements?

Potential enhancements include interview coaching, analytics dashboards, real-time feedback and further model optimization.

## 6. Difficult Questions

### Q20. Is the system production-ready?

Production readiness requires verified implementation, integration testing, security validation, performance benchmarking and deployment checks. Documentation alone does not establish production readiness.

### Q21. What happens if an AI module produces an incorrect result?

The result should be reviewed, the underlying issue investigated and the relevant component tested and corrected. Human review is important for consequential hiring decisions.

### Q22. What is the biggest challenge in this project?

A major challenge is processing different resume formats and accurately matching candidate information with job requirements while maintaining consistent and explainable evaluations.

## 7. Answering Questions Professionally

- Understand the question before answering.
- Give a direct answer first.
- Explain with a practical example.
- Avoid guessing.
- Distinguish implemented features from planned features.
- Be transparent about limitations.
