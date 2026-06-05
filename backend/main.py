from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. This creates your backend server application
app = FastAPI()

# 2. This fixes the CORS error before it even happens. 
# It tells your backend to allow your frontend to talk to it.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all frontend websites to connect for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. This is a "Mock API" (a fake endpoint). 
# When someone visits your backend, it sends a friendly greeting.
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