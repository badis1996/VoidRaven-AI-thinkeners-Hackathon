from fastapi import APIRouter

from app.api.v1.endpoints import candidates

api_router = APIRouter()

api_router.include_router(
    candidates.router, prefix="/candidates", tags=["candidates"]
) 