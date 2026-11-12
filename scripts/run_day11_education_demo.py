from src.education_certification import (
    extract_education,
    extract_certifications,
    education_relevance,
)

import json


print("=" * 65)
print("DAY 11 - EDUCATION & CERTIFICATION PARSING")
print("=" * 65)


resume_text = """
EDUCATION

MCA in Computer Science
ABC University
2025

B.Tech in Computer Science Engineering
XYZ College
2022

CERTIFICATIONS

Google Data Analytics Certificate
AWS Certified Cloud Practitioner
Python Programming Certificate
"""


# ---------------------------------------------------------
# EDUCATION EXTRACTION
# ---------------------------------------------------------

education = extract_education(resume_text)

print("\nEDUCATION PROFILE")
print("-" * 65)

print(json.dumps(
    education,
    indent=4
))


# ---------------------------------------------------------
# CERTIFICATION EXTRACTION
# ---------------------------------------------------------

certifications = extract_certifications(
    resume_text
)

print("\nCERTIFICATIONS")
print("-" * 65)

print(json.dumps(
    certifications,
    indent=4
))


# ---------------------------------------------------------
# EDUCATION RELEVANCE
# ---------------------------------------------------------

relevance = education_relevance(
    education,
    "Data Analyst"
)

print("\nEDUCATION RELEVANCE")
print("-" * 65)

print(json.dumps(
    relevance,
    indent=4
))


# ---------------------------------------------------------
# FINAL STRUCTURED ACADEMIC PROFILE
# ---------------------------------------------------------

academic_profile = {
    "education": education,
    "certifications": certifications,
    "relevance": relevance
}

print("\nSTRUCTURED ACADEMIC PROFILE")
print("-" * 65)

print(json.dumps(
    academic_profile,
    indent=4
))


print("\n" + "=" * 65)
print("DAY 11 EDUCATION & CERTIFICATION TEST COMPLETED")
print("=" * 65)