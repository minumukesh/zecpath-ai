# Zecpath AI - Developer Onboarding Guide

## 1. Welcome

This guide helps developers understand the Zecpath AI repository, run the project, test components and safely extend existing functionality.

## 2. Development Environment

Known development environment:
- Operating System: Windows.
- Language: Python.
- Virtual environment: venv.
- Testing framework: pytest.
- Editor: Visual Studio Code.

Check installed Python:

```powershell
python --version
```

Check pip:

```powershell
python -m pip --version
```

## 3. Project Structure

Important project directories:

| Directory | Purpose |
|---|---|
| src/ | Application and AI source modules |
| tests/ | Automated test cases |
| docs/ | Project documentation |
| data/ | Supporting project data |
| outputs/ | Generated reports and results |

The exact contents of each directory should be inspected in the current repository.

## 4. Activate Virtual Environment

From the project root in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If the environment is already active, do not activate it again unnecessarily.

## 5. Install Dependencies

First inspect the dependency file:

```powershell
Get-ChildItem requirements*.txt, pyproject.toml, setup.py -ErrorAction SilentlyContinue
```

If requirements.txt exists:

```powershell
python -m pip install -r requirements.txt
```

Use the dependency manifest maintained by the project. Do not invent or install unrelated packages.

## 6. Understand the ATS Pipeline

Start by inspecting:
- src/ats_pipeline/pipeline.py
- src/ats_scoring/engine.py
- src/candidate_ranking/engine.py
- src/ats_api/api.py

Understand how data moves through extraction, matching, scoring and ranking before changing code.

## 7. Run Automated Tests

Run all tests:

```powershell
python -m pytest -v
```

Run a specific test file:

```powershell
python -m pytest -v path/to/test_file.py
```

## 8. Development Workflow

```text
Understand Requirement
        |
        v
Locate Existing Component
        |
        v
Inspect Current Implementation
        |
        v
Reuse Existing Logic
        |
        v
Make a Small Change
        |
        v
Run Targeted Tests
        |
        v
Run Full Test Suite
        |
        v
Update Documentation
```

## 9. Important Development Rules

1. Do not create a duplicate ATS scoring engine.
2. Do not recalculate ATS scores inside candidate ranking.
3. Reuse the existing pipeline where possible.
4. Preserve existing API contracts unless a change is required and approved.
5. Validate missing and invalid input.
6. Add tests for new behavior.
7. Run relevant tests after modifications.
8. Document important changes.

## 10. Debugging Guidelines

- Run the relevant test first.
- Read the complete error message.
- Locate the failing module.
- Inspect the implementation.
- Make the smallest necessary correction.
- Run the targeted test again.
- Run the full suite after the correction.

Do not modify unrelated modules to hide a failure.

## 11. Git Workflow

Before committing changes:

```powershell
git status
git diff
```

Review changes before creating a commit. Follow the repository contribution and branch rules if they are defined.

## 12. Developer Completion Checklist

- [ ] Development environment activated.
- [ ] Dependencies inspected and installed.
- [ ] Project structure understood.
- [ ] Existing ATS pipeline inspected.
- [ ] Relevant tests executed.
- [ ] New changes tested.
- [ ] Documentation updated.
- [ ] Changes reviewed before commit.

## 13. Conclusion

Developers should understand existing module responsibilities and preserve the separation between extraction, scoring, ranking and decision support.
