import uuid

def create_interview_payload(resume_data):

    return {
        "session_id": str(uuid.uuid4()),
        "candidate_name": resume_data.get("name", "Candidate"),
        "domain": resume_data.get("domain", "Software Developer"),
        "skills": resume_data.get("skills", []),
        "experience_level": resume_data.get("experience_level", "Beginner"),
        "years_of_experience": resume_data.get("years_of_experience", 0),
        "education": resume_data.get("education", ""),
        "key_projects": resume_data.get("projects", []),
        "certifications": resume_data.get("certifications", []),
        "company_type": "General",
        "interview_tone": "Friendly"
    }