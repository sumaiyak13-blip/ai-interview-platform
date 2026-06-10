import os
import io
import json
import pdfplumber
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google import genai

# 1. Load configuration environment variables
load_dotenv()

app = FastAPI(title="Streamlit Skill Gap Engine")

# ✅ Connects smoothly with your local ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini Client securely
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Missing GEMINI_API_KEY inside your .env configuration.")

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    raise RuntimeError(f"Initialization Error: {e}")


@app.get("/")
def read_root():
    return {"message": "Streamlit Backend Engine is Active!"}


# 🎯 MATCHES YOUR STREAMLIT SCRIPT: http://127.0.0.1:8000/analyze-skills
@app.post("/analyze-skills")
async def analyze_skills(target_job: str = Form(...), file: UploadFile = File(...)):
    try:
        # Extract text from your uploaded PDF file
        pdf_bytes = await file.read()
        resume_text = ""
        
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    resume_text += text + "\n"

        # Fallback if the text extraction yields nothing
        if not resume_text.strip():
            return {
                "detected_gaps": ["Unable to extract text from your document."],
                "action_items": ["Please save your file as a standard text-based PDF and re-upload."],
                "current_eligibility": ["Scanned/Image Format Detected"]
            }

        # The prompt that builds your specialized clinical metrics matching your script
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

        # Fetch evaluation details via Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        # Sanitize and clean markdown formatting blocks if present
        clean_text = response.text.strip()
        if clean_text.startswith("```"):
            clean_text = clean_text.split("```")[1]
            if clean_text.startswith("json"):
                clean_text = clean_text[4:]
        clean_text = clean_text.strip()

        # Convert string output to JSON fields that your lines 91-93 read
        analysis = json.loads(clean_text)
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

if __name__ == "__main__":
    # Force it to run on local loopback to guarantee Streamlit connection
    uvicorn.run("skill_gap_backend:app", host="127.0.0.1", port=8000, reload=True)
