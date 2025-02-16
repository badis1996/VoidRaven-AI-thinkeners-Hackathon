from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import selectinload
import base64
import json
import httpx
import os
from pydantic import BaseModel

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
    VapiTranscriptResponse,
)
from app.services.resume_analysis.resume_agent import ResumeAnalysisAgent
from app.services.transcript_analysis.transcript_agent import TranscriptAnalysisAgent

resume_agent = ResumeAnalysisAgent()
transcript_agent = TranscriptAnalysisAgent()
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
            pdf_data = base64.b64encode(cv_file.file.read()).decode('utf-8')
            cv_data = resume_agent.read_resume(pdf_data)
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

class VapiTranscriptRequest(BaseModel):
    email: str
    call_id: str

@router.post("/vapi-transcript", response_model=VapiTranscriptResponse)
async def fetch_vapi_transcript(
    *,
    db: AsyncSession = Depends(get_db),
    request: VapiTranscriptRequest,
) -> Any:
    """Fetch transcript from Vapi API and update interview record."""
    # Get the candidate
    result = await db.execute(
        select(CandidateModel).where(CandidateModel.email == request.email)
    )
    candidate = result.scalar_one_or_none()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    # Fetch transcript from Vapi
    vapi_token = os.getenv("VAPI_TOKEN")
    if not vapi_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="VAPI_TOKEN not configured",
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.vapi.ai/call/{request.call_id}",
            headers={"Authorization": f"Bearer {vapi_token}"},
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch transcript from Vapi: {response.text}",
            )
        
        vapi_data = response.json()
        transcript = vapi_data.get("transcript")
        if not transcript:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No transcript found in Vapi response",
            )

    # Analyze the transcript
    try:
        evaluation = transcript_agent.analyse_transcript(transcript)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing transcript: {str(e)}",
        )

    # Create or update interview
    try:
        result = await db.execute(
            select(InterviewModel)
            .where(InterviewModel.candidate_id == candidate.id)
        )
        interview = result.scalar_one_or_none()
        
        if not interview:
            interview = InterviewModel(
                candidate_id=candidate.id,
                transcript=transcript,
                audio_url=vapi_data.get("recordingUrl"),
                evaluation=evaluation
            )
            db.add(interview)
        else:
            interview.transcript = transcript
            interview.audio_url = vapi_data.get("recordingUrl")
            interview.evaluation = evaluation
        
        await db.commit()
        await db.refresh(interview)
        
        # Return only transcript and evaluation
        return VapiTranscriptResponse(
            transcript=transcript,
            evaluation=evaluation
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving interview: {str(e)}",
        ) 