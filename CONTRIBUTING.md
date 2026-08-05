# Zecpath AI – Code Standards & Documentation Guidelines

## 1. Python Code Standards

- Follow PEP 8 coding standards.
- Use meaningful variable and function names.
- Use 4 spaces for indentation.
- Keep functions small and focused on one task.
- Avoid unnecessary duplicate code.
- Organize functionality into appropriate modules.

## 2. Naming Conventions

- Variables: snake_case
- Functions: snake_case
- Classes: PascalCase
- Constants: UPPER_CASE
- Python files: snake_case

Example:

```python
candidate_score = 85

def calculate_ats_score():
    pass

class ResumeParser:
    pass

## 3. Documentation Standards

Every important function should contain a docstring explaining:

- Purpose of the function
- Parameters
- Return value

Example:

```python
def calculate_score(resume_text):
    """
    Calculate the candidate score from resume data.

    Args:
        resume_text (str): Extracted resume content.

    Returns:
        float: Calculated candidate score.
    """
    pass
```

## 4. Logging Standards

Use the centralized logger from `utils/logger.py`.

Important AI activities should be logged, including:

- Resume parsing
- ATS processing
- Candidate screening
- Interview evaluation
- Candidate scoring
- System errors

## 5. Testing Standards

- Tests must be stored inside the `tests/` directory.
- Test files should begin with `test_`.
- Use pytest for unit testing.
- New AI modules should have corresponding tests.

## 6. Git Standards

Use clear and meaningful commit messages.

Examples:

- `Add AI project structure`
- `Add logging configuration`
- `Add ATS engine tests`
- `Update project documentation`