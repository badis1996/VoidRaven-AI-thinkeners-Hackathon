from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl

class InterviewBase(BaseModel):
    """Base Pydantic model for Interview."""
    candidate_id: UUID
    transcript: Optional[str] = None
    audio_url: Optional[HttpUrl] = None
    video_path: Optional[str] = None
    audio_path: Optional[str] = None

class InterviewCreate(InterviewBase):
    """Pydantic model for creating an Interview."""
    pass

class InterviewUpdate(BaseModel):
    """Pydantic model for updating an Interview."""
    transcript: Optional[str] = None
    audio_url: Optional[HttpUrl] = None
    video_path: Optional[str] = None
    audio_path: Optional[str] = None

class InterviewInDB(InterviewBase):
    """Pydantic model for Interview in database."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic model configuration."""
        from_attributes = True

class Interview(InterviewInDB):
    """Pydantic model for Interview response."""
    pass 