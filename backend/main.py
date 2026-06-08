import os
import io
import pdfplumber
import json
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google import genai

from resume_processor import create_resume_summary

# 1. Load the .env configuration
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

app = FastAPI(title="AI Mock Interview - Core Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Missing GEMINI_API_KEY.")

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    raise RuntimeError(f"Initialization Error: {e}")


@app.get("/")
def read_root():
    return {"message": "AI Backend is active!"}


@app.post("/analyze-skills")
async def analyze_skills(target_job: str = Form(...), file: UploadFile = File(...)):
    try:
        # Step A: Robust layout text extraction using pdfplumber
        pdf_bytes = await file.read()
        resume_text = ""
        
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    resume_text += text + "\n"

        # Check if text extraction completely failed (e.g., scanned image)
        if not resume_text.strip():
            return {
                "target_job": target_job,
                "detected_gaps": ["Unable to extract text. Your PDF might be a scanned image/photo."],
                "action_items": ["Please use a text-based PDF generated directly from Word or Canva."],
                "current_eligibility": ["Scanned Document Detected"]
            }

        # Step B: Optimized Prompt
        prompt = f"""
        You are an expert career recruiter. Analyze the following resume text against the target job: '{target_job}'.
        
        Resume Text:
        {resume_text}
        
        You must return a valid JSON object. Do not include markdown wraps like ```json. 
        Use this exact structural template:
        {{
            "detected_gaps": ["gap 1", "gap 2"],
            "action_items": ["action 1", "action 2"],
            "current_eligibility": ["role 1", "role 2"]
        }}
        """

        # Step C: Generate content
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        # Step D: Clean structural markdown strings
        clean_text = response.text.strip()
        if clean_text.startswith("```"):
            clean_text = clean_text.split("```")[1]
            if clean_text.startswith("json"):
                clean_text = clean_text[4:]
        clean_text = clean_text.strip()

        # Step E: Safely parse JSON output
        analysis = json.loads(clean_text)
        return {
            "target_job": target_job,
            "detected_gaps": analysis.get("detected_gaps", ["No gaps identified."]),
            "action_items": analysis.get("action_items", ["Profile alignment looks good."]),
            "current_eligibility": analysis.get("current_eligibility", ["General Clinical Roles"])
        }

    except Exception as e:
        return {
            "target_job": target_job,
            "detected_gaps": ["Parsing issue encountered. Review text structure."],
            "action_items": ["Verify file translation integrity or try a simpler format."],
            "current_eligibility": ["Alternative Assessment Required"]
        }
    
    @app.post("/extract-resume")
async def extract_resume(file: UploadFile = File(...)):

    try:
        pdf_bytes = await file.read()

        resume_text = ""

        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    resume_text += text + "\n"

        prompt = f"""
        Extract the following information from this resume.

        Resume:
        {resume_text}

        Return ONLY valid JSON.

        Format:

        {{
            "name": "",
            "education": "",
            "skills": [],
            "projects": [],
            "certifications": [],
            "years_of_experience": 0
        }}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        clean_text = response.text.strip()

        if clean_text.startswith("```"):
            clean_text = clean_text.split("```")[1]

            if clean_text.startswith("json"):
                clean_text = clean_text[4:]

        clean_text = clean_text.strip()

        extracted_data = json.loads(clean_text)

        return extracted_data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
