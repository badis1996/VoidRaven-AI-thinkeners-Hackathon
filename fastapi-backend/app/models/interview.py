from sqlalchemy import Column, String, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.models.base import BaseModel

class Interview(BaseModel):
    """Interview model for storing interview sessions."""

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transcript = Column(Text, nullable=True)
    audio_url = Column(String(500), nullable=True)  # URL from VAPI
    video_path = Column(String(500), nullable=True)  # Local storage path
    audio_path = Column(String(500), nullable=True)  # Local storage path
    evaluation = Column(JSON, nullable=True)  # Transcript analysis results
    
    # Foreign Keys
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidate.id"), nullable=False)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="interviews")
    questions = relationship("Question", back_populates="interview", cascade="all, delete-orphan") 