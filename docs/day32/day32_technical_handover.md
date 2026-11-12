# Zecpath AI - Technical Handover

## Project purpose
The screening system processes candidate information and supports recruiters
with structured evaluation results.

## High-level workflow
Candidate Resume + Job Description
→ Resume Extraction and JD Parsing
→ Candidate Analysis
→ ATS Scoring
→ Candidate Ranking and Eligibility
→ Screening Report
→ Recruiter Review

Verify the actual code paths before describing every stage as integrated.

## API design
- Validate incoming requests.
- Validate uploaded file types and required parameters.
- Pass valid requests to the existing backend and ATS pipeline.
- Return structured results or job status.
- Handle failures with consistent error responses.
- Log errors without exposing private candidate information.

Use the project's existing API routes and schemas. Do not assume an endpoint
exists unless it is present in the source code.

## Run instructions
1. Open the project root in a terminal.
2. Activate the project's virtual environment.
3. Install dependencies from the project's existing dependency file.
4. Run the demo and automated tests.
5. Review the generated JSON and Markdown reports.

## Handover checklist
- [ ] Source code reviewed
- [ ] Dependencies documented
- [ ] API routes verified
- [ ] Automated tests passed
- [ ] Error handling reviewed
- [ ] Configuration documented
- [ ] Real demo screenshots saved
- [ ] Known limitations recorded
- [ ] Deployment verified separately, if applicable

## Limitations
A successful local demo or test suite does not prove production deployment.
The standalone Day 32 demo uses a keyword-overlap indicator and is not the
official ATS scoring engine. Human review remains necessary for uncertain cases.
