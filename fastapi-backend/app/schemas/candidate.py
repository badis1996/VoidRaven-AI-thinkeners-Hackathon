from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID
from fastapi import UploadFile
from pydantic import BaseModel, EmailStr, Field

class CandidateBase(BaseModel):
    """Base Pydantic model for Candidate."""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    cv_data: Optional[Dict[str, Any]] = None

class CandidateCreate(BaseModel):
    """Pydantic model for creating a Candidate."""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    cv_file: Optional[UploadFile] = None

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

class QuestionCreate(BaseModel):
    """Pydantic model for creating a Question."""
    content: str
    answer: str

class QuestionResponse(QuestionCreate):
    """Pydantic model for Question response."""
    id: UUID
    interview_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic model configuration."""
        from_attributes = True

class InterviewDataUpdate(BaseModel):
    """Pydantic model for updating interview data."""
    email: EmailStr
    audio_url: Optional[str] = None
    transcript: str
    questions: Optional[List[QuestionCreate]] = []

class InterviewResponse(BaseModel):
    """Pydantic model for Interview response."""
    id: UUID
    candidate_id: UUID
    transcript: str
    audio_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic model configuration."""
        from_attributes = True

class TranscriptResponse(BaseModel):
    """Pydantic model for transcript response."""
    email: EmailStr
    transcript: str
    created_at: datetime 