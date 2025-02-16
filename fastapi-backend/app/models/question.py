from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.models.base import BaseModel

class Question(BaseModel):
    """Question model for storing interview questions and answers."""

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    
    # Foreign Keys
    interview_id = Column(UUID(as_uuid=True), ForeignKey("interview.id"), nullable=False)
    
    # Relationships
    interview = relationship("Interview", back_populates="questions") 