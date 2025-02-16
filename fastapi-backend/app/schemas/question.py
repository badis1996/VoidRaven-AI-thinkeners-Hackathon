from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class QuestionBase(BaseModel):
    """Base Pydantic model for Question."""
    interview_id: UUID
    question: str
    answer: Optional[str] = None

class QuestionCreate(QuestionBase):
    """Pydantic model for creating a Question."""
    pass

class QuestionUpdate(BaseModel):
    """Pydantic model for updating a Question."""
    question: Optional[str] = None
    answer: Optional[str] = None

class QuestionInDB(QuestionBase):
    """Pydantic model for Question in database."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic model configuration."""
        from_attributes = True

class Question(QuestionInDB):
    """Pydantic model for Question response."""
    pass 