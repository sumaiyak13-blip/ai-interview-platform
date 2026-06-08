#Integrating Gemini into FastAPI
# main.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai


# Load environment variables from the .env file
#load_dotenv()
# Temporary Debugging Code
load_dotenv()
print(f"--- DEBUG: API Key found in environment: {os.environ.get('GEMINI_API_KEY')} ---")
app = FastAPI(
    title="AI Mock Interview - Core Engine",
    description="Backend service managing resume analysis and dynamic question generation."
)

# Initialize the official Google GenAI Client
try:
    # This automatically grabs os.environ["GEMINI_API_KEY"]
    ai_client = genai.Client()
except Exception as e:
    raise RuntimeError(f"Initialization Error: Ensure GEMINI_API_KEY is set. Details: {e}")


# Define structural request models for your endpoints
class InterviewSetupRequest(BaseModel):
    job_title: str
    experience_level: str  # e.g., Junior, Mid, Senior
    resume_summary: str

@app.get("/health")
def health_check():
    """Simple endpoint to verify the server is running."""
    return {"status": "healthy", "engine": "Gemini API Active"}


@app.post("/generate-questions")
async def generate_interview_questions(payload: InterviewSetupRequest):
    """
    Core AI engine endpoint to generate tailored behavioral questions 
    based on a candidate's profile.
    """
    # Construct a highly targeted system-level directive within the prompt
    prompt = f"""
    You are an elite technical interviewer. Generate exactly 3 challenging interview questions 
    tailored specifically for a {payload.experience_level}-level {payload.job_title} role.
    
    Incorporate elements or test concepts related to this candidate's background summary:
    "{payload.resume_summary}"
    
    Format the output cleanly as a bulleted list. Go straight to the questions without pleasantries.
    """
    
    try:
        # Call the default fast text model
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        return {
            "success": True,
            "questions": response.text
        }
        
    except Exception as e:
        # Catch API issues, rate limits, or bad requests gracefully
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")