from resume_mapper import create_interview_payload

resume_data = {
    "name": "John Doe",
    "domain": "Machine Learning Engineer",
    "skills": ["Python", "FastAPI", "Machine Learning"],
    "education": "B.Tech Computer Science",
    "projects": [
        "AI Interview System",
        "Resume Analyzer"
    ],
    "certifications": [
        "AWS Practitioner"
    ],
    "years_of_experience": 2,
    "experience_level": "Intermediate"
}

payload = create_interview_payload(resume_data)

print(payload)