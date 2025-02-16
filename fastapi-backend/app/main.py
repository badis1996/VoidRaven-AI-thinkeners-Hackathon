from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router

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

    # Add API router
    application.include_router(api_router, prefix=settings.API_V1_STR)

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)