from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pypdf
import io

# 1. This creates your backend server application
app = FastAPI()

# 2. This fixes the CORS error before it even happens. 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. This is a "Mock API" (a fake endpoint). 
@app.get("/")
def read_root():
    return {"message": "Hello Member 1! Your backend skeleton is officially alive!"}

# 4. Another Mock API for your teammates to use later for testing the upload
@app.get("/api/mock-resume")
def mock_resume():
    return {
        "status": "success",
        "ats_score": 85,
        "skills_found": ["Python", "React", "Communication"]
    }

# 5. NEW: Your Skill Analyzer feature!
@app.post("/analyze-skills")
async def analyze_skills(target_job: str = Form(...), file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
    extracted_text = ""
    for page in pdf_reader.pages:
        extracted_text += page.extract_text() or ""
        
    return {
        "target_job": target_job,
        "detected_gaps": [
            "Missing hands-on experience with cloud deployment pipelines (CI/CD).",
            "Lack of specialized automated testing workflows mentioned in the history."
        ],
        "action_items": [
            "Take a short credential course covering cloud architecture mechanics.",
            "Revise the experience text to emphasize metrics (e.g., 'Improved performance by 20%')."
        ],
        "current_eligibility": [
            "Junior Project Engineer",
            "Data Specialist / QA Tester"
        ]
    }