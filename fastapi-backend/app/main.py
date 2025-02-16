from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add routers
    # TODO: Import and include routers for different API endpoints
    # application.include_router(interviews_router, prefix="/api/v1/interviews")
    # application.include_router(assessments_router, prefix="/api/v1/assessments")
    # application.include_router(actions_router, prefix="/api/v1/actions")

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