from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class CandidateBase(BaseModel):
    """Base Pydantic model for Candidate."""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    cv_data: Optional[Dict[str, Any]] = None

class CandidateCreate(CandidateBase):
    """Pydantic model for creating a Candidate."""
    cv_file: Optional[str] = Field(None, description="Base64 encoded PDF file")

class CandidateUpdate(BaseModel):
    """Pydantic model for updating a Candidate."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    cv_data: Optional[Dict[str, Any]] = None

class CandidateInDB(CandidateBase):
    """Pydantic model for Candidate in database."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic model configuration."""
        from_attributes = True

class Candidate(CandidateInDB):
    """Pydantic model for Candidate response."""
    pass

class InterviewDataUpdate(BaseModel):
    """Pydantic model for updating interview data."""
    email: EmailStr
    audio_url: str
    transcript: str

class TranscriptResponse(BaseModel):
    """Pydantic model for transcript response."""
    email: EmailStr
    transcript: str
    created_at: datetime 