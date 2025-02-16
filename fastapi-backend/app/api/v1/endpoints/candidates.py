from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
import base64
import json

from app.core.database import get_db
from app.models.candidate import Candidate as CandidateModel
from app.models.interview import Interview as InterviewModel
from app.schemas.candidate import (
    Candidate,
    CandidateCreate,
    InterviewDataUpdate,
    TranscriptResponse,
)

router = APIRouter()

@router.post("/", response_model=Candidate, status_code=status.HTTP_201_CREATED)
async def create_candidate(
    *,
    db: AsyncSession = Depends(get_db),
    candidate_in: CandidateCreate,
) -> Any:
    """Create new candidate with CV."""
    # Check if candidate with email already exists
    result = await db.execute(
        select(CandidateModel).where(CandidateModel.email == candidate_in.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate with this email already exists",
        )

    # Process CV file if provided
    cv_data = {}
    if candidate_in.cv_file:
        try:
            # Store the base64 encoded PDF
            cv_data = {
                "pdf_content": candidate_in.cv_file,
                "mime_type": "application/pdf"
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error processing CV file: {str(e)}",
            )

    # Create new candidate
    db_obj = CandidateModel(
        name=candidate_in.name,
        email=candidate_in.email,
        cv_data=cv_data,
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.post("/interview", status_code=status.HTTP_200_OK)
async def update_interview_data(
    *,
    db: AsyncSession = Depends(get_db),
    interview_data: InterviewDataUpdate,
) -> Any:
    """Update interview data for a candidate."""
    # Find candidate
    result = await db.execute(
        select(CandidateModel).where(CandidateModel.email == interview_data.email)
    )
    candidate = result.scalar_one_or_none()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    # Create or update interview
    result = await db.execute(
        select(InterviewModel).where(InterviewModel.candidate_id == candidate.id)
    )
    interview = result.scalar_one_or_none()

    if interview:
        # Update existing interview
        interview.audio_url = interview_data.audio_url
        interview.transcript = interview_data.transcript
    else:
        # Create new interview
        interview = InterviewModel(
            candidate_id=candidate.id,
            audio_url=interview_data.audio_url,
            transcript=interview_data.transcript,
        )
        db.add(interview)

    await db.commit()
    await db.refresh(interview)
    return {"message": "Interview data updated successfully"}

@router.get("/transcript/{email}", response_model=TranscriptResponse)
async def get_transcript(
    email: str,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get interview transcript by candidate email."""
    # Find candidate and their latest interview
    result = await db.execute(
        select(CandidateModel, InterviewModel)
        .join(InterviewModel)
        .where(CandidateModel.email == email)
        .order_by(InterviewModel.created_at.desc())
    )
    row = result.first()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No interview found for this email",
        )

    candidate, interview = row
    return TranscriptResponse(
        email=candidate.email,
        transcript=interview.transcript,
        created_at=interview.created_at,
    ) 