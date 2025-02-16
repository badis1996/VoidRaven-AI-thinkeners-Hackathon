from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.models.base import BaseModel

class Candidate(BaseModel):
    """Candidate model for storing applicant information."""

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    cv_data = Column(JSON, nullable=True)

    # Relationships
    interviews = relationship("Interview", back_populates="candidate", cascade="all, delete-orphan") 