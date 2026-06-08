def create_resume_summary(resume_data):

    summary = f"""
    Candidate Name: {resume_data['name']}

    Education:
    {resume_data['education']}

    Skills:
    {", ".join(resume_data['skills'])}

    Projects:
    {", ".join(resume_data['projects'])}

    Certifications:
    {", ".join(resume_data['certifications'])}

    Years of Experience:
    {resume_data['years_of_experience']}
    """

    return summary