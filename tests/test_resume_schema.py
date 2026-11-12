import json
from pathlib import Path

from jsonschema import validate


BASE_DIR = Path(__file__).resolve().parent.parent

SCHEMA_PATH = BASE_DIR / "schemas" / "resume_schema.json"
RESUMES_PATH = BASE_DIR / "data" / "resumes" / "structured"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def test_resume_01_schema():
    schema = load_json(SCHEMA_PATH)
    resume = load_json(RESUMES_PATH / "resume_01.json")

    validate(instance=resume, schema=schema)


def test_resume_02_schema():
    schema = load_json(SCHEMA_PATH)
    resume = load_json(RESUMES_PATH / "resume_02.json")

    validate(instance=resume, schema=schema)
