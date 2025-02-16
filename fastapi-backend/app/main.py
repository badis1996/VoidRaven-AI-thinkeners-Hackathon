from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import audio_analysis
import base64
from dotenv import load_dotenv

from app.api.v1.endpoints import resume_analysis

# Load environment variables from .env file
load_dotenv()

# Create the FastAPI application
app = FastAPI(
    title="AI Assessment Agent API",
    description="Backend API for the AI-powered university admissions interview platform",
    version="0.1.0",
)

# Add routers
# TODO: Import and include routers for different API endpoints
# application.include_router(interviews_router, prefix="/api/v1/interviews")
# application.include_router(assessments_router, prefix="/api/v1/assessments")
# application.include_router(actions_router, prefix="/api/v1/actions")
app.include_router(
    audio_analysis.router,
    prefix="/api/v1/audio",
    tags=["audio"]
)
app.include_router(
    resume_analysis.router, 
    prefix="/api/v1/resume", 
    tags=["resume"]
)

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "AI Assessment Agent API",
        "version": "0.1.0",
        "status": "operational",
    }

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "AI Assessment Agent API",
        "version": "0.1.0",
        "status": "operational",
    }

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
