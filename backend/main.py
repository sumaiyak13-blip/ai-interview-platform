import os
import io
import pdfplumber
import json
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google import genai

# 1. Load the .env configuration safely
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

app = FastAPI(title="AI Mock Interview - Unified Master Core Engine")

# ✅ Smooth connection middleware for both setups
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Missing GEMINI_API_KEY inside your local configuration.")

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    raise RuntimeError(f"Initialization Error: {e}")


@app.get("/")
def read_root():
    return {"message": "AI Unified Master Backend is active!"}


# ==========================================
# 🌟 ROUTE 1: ALFIYA'S SKILL GAP ENGINE (CLEANED)
# ==========================================
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
                "detected_gaps": ["Unable to extract text. Your PDF might be a scanned image/photo."],
                "action_items": ["Please use a text-based PDF generated directly from Word or Canva."],
                "current_eligibility": ["Scanned Document Detected"]
            }

        # Step B: Optimized Prompt for Skill Gap Dashboard
        prompt = f"""
        You are an elite talent recruiter and senior clinical healthcare consultant.
        Analyze this professional background profile against the target assignment position: '{target_job}'.
        
        Resume Text Data:
        {resume_text}
        
        You must return a raw JSON object matching this schema structure. Do not include markdown wraps like ```json:
        {{
            "detected_gaps": ["gap 1", "gap 2"],
            "action_items": ["action item 1", "action item 2"],
            "current_eligibility": ["eligibility status assessment description"]
        }}
        """

        # Step C: Generate content via Gemini
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

        # Step E: Safely parse JSON output for Streamlit App lines 91-93
        analysis = json.loads(clean_text)
        
        # ✨ EXACT THREE KEYS EXPECTED BY YOUR FRONTEND SCRIPT WITH NO EXTRAS
        return {
            "detected_gaps": analysis.get("detected_gaps", ["No significant critical skill mismatches found."]),
            "action_items": analysis.get("action_items", ["Your current career path looks tightly aligned."]),
            "current_eligibility": analysis.get("current_eligibility", ["General Fitness Baseline Verified"])
        }

    except Exception as e:
        return {
            "detected_gaps": [f"System evaluation error: {str(e)}"],
            "action_items": ["Attempt a simpler document template file format update."],
            "current_eligibility": ["Alternative Processing Queue Required"]
        }


# ==========================================
# 🌟 ROUTE 2: TEAMMATES' RESUME EXTRACTION ROUTE
# ==========================================
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

        Return ONLY valid JSON. Do not include markdown wraps like ```json.

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)