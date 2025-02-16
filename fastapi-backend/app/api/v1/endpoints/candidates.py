from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import selectinload
import base64
import json

from app.core.database import get_db
from app.models.candidate import Candidate as CandidateModel
from app.models.interview import Interview as InterviewModel
from app.models.question import Question
from app.schemas.candidate import (
    Candidate,
    CandidateCreate,
    InterviewDataUpdate,
    InterviewResponse,
    TranscriptResponse,
)

router = APIRouter()

@router.post("/", response_model=Candidate, status_code=status.HTTP_201_CREATED)
async def create_candidate(
    *,
    db: AsyncSession = Depends(get_db),
    name: str = Form(...),
    email: str = Form(...),
    cv_file: UploadFile = File(None),
) -> Any:
    """Create new candidate with CV."""
    # Check if candidate with email already exists
    result = await db.execute(
        select(CandidateModel).where(CandidateModel.email == email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate with this email already exists",
        )

    # Process CV file if provided
    cv_data = {}
    if cv_file:
        try:
            # Read the PDF file content
            content = await cv_file.read()
            # Store the PDF content and metadata
            cv_data = {
                "pdf_content": base64.b64encode(content).decode('utf-8'),
                "filename": cv_file.filename,
                "mime_type": cv_file.content_type
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error processing CV file: {str(e)}",
            )

    # Create new candidate
    db_obj = CandidateModel(
        name=name,
        email=email,
        cv_data=cv_data,
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.post("/interview", response_model=InterviewResponse, status_code=status.HTTP_200_OK)
async def update_interview_data(
    *,
    db: AsyncSession = Depends(get_db),
    interview_data: InterviewDataUpdate,
) -> Any:
    """Update interview data for a candidate."""
    # Get the candidate
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
        select(InterviewModel)
        .where(InterviewModel.candidate_id == candidate.id)
        .options(selectinload(InterviewModel.questions))
    )
    interview = result.scalar_one_or_none()
    
    if not interview:
        interview = InterviewModel(
            candidate_id=candidate.id,
            transcript=interview_data.transcript
        )
        db.add(interview)
    else:
        interview.transcript = interview_data.transcript
    
    await db.flush()
    
    # Add questions if provided
    if interview_data.questions:
        for q in interview_data.questions:
            question = Question(
                interview_id=interview.id,
                content=q.content,
                answer=q.answer
            )
            db.add(question)
    
    await db.commit()
    await db.refresh(interview)
    
    # Reload interview with questions
    result = await db.execute(
        select(InterviewModel)
        .where(InterviewModel.id == interview.id)
        .options(selectinload(InterviewModel.questions))
    )
    interview = result.scalar_one()
    return interview

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
        .options(selectinload(InterviewModel.questions))
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