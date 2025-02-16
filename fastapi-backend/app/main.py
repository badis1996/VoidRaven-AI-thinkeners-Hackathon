from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.core.config import settings
from app.api.v1.api import api_router
from app.api.v1.endpoints import audio_analysis, resume_analysis

# Load environment variables from .env file
load_dotenv()

def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="AI Assessment Agent API",
        description="Backend API for the AI-powered university admissions interview platform",
        version="0.1.0",
    )

    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add API routers
    application.include_router(api_router, prefix=settings.API_V1_STR)
    application.include_router(
        audio_analysis.router,
        prefix="/api/v1/audio",
        tags=["audio"]
    )
    application.include_router(
        resume_analysis.router, 
        prefix="/api/v1/resume", 
        tags=["resume"]
    )

    @application.get("/")
    async def root():
        """Root endpoint returning API information."""
        return {
            "name": "AI Assessment Agent API",
            "version": "0.1.0",
            "status": "operational",
        }

    return application

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
