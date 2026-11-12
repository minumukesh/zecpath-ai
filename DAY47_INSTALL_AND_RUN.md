# Day 47 installation and execution

Copy the package contents into the root of your existing `ZECPATH-AI` project. Do not overwrite existing files. The new engine has a new filename and does not modify Days 44-46.

From the project root, with the existing virtual environment activated:

```powershell
python -m unittest discover -s tests\day47 -v
python run_day47_scoring_demo.py
python -m pytest -q
```

Expected new outputs:
- `outputs/day47/technical_skill_evaluation.json`
- `outputs/day47/technical_skill_evaluation.md`

Review the report. The included demo answers are synthetic examples, not actual candidate evaluations. Human review is required.
