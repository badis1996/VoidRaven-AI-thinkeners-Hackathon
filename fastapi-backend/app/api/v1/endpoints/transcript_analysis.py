from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, Any, List
import re

from app.core.database import get_db
from app.models.interview import Interview
from app.models.question import Question
from app.services.transcript_analysis.transcript_agent import TranscriptAnalysisAgent

router = APIRouter()
transcript_agent = TranscriptAnalysisAgent()

def extract_qa_pairs(transcript: str) -> List[Dict[str, str]]:
    """Extract question-answer pairs from the transcript."""
    # Use regex to find all AI and User exchanges
    # Pattern looks for "AI:" followed by any text until "User:" or end of string
    qa_pattern = r'AI:(.*?)(?=AI:|User:|$)'
    answer_pattern = r'User:(.*?)(?=AI:|User:|$)'
    
    # Find all AI questions
    questions = [q.strip() for q in re.findall(qa_pattern, transcript, re.DOTALL)]
    # Find all User answers
    answers = [a.strip() for a in re.findall(answer_pattern, transcript, re.DOTALL)]
    
    # Pair questions with their corresponding answers
    qa_pairs = []
    for i in range(len(questions)):
        # Only add pairs where we have both a question and an answer
        if i < len(answers):
            # Clean up the text by removing extra whitespace and newlines
            question = ' '.join(questions[i].split())
            answer = ' '.join(answers[i].split())
            
            # Only add non-empty pairs
            if question and answer:
                qa_pairs.append({
                    "question": question,
                    "answer": answer
                })
    
    return qa_pairs

@router.post("/analyze/{interview_id}")
async def analyze_transcript(
    interview_id: str,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Analyze interview transcript and store Q&A pairs."""
    # Get interview from database
    result = await db.execute(
        select(Interview).where(Interview.id == interview_id)
    )
    interview = result.scalar_one_or_none()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    if not interview.transcript:
        raise HTTPException(status_code=400, detail="No transcript available for analysis")
    
    # Analyze transcript
    analysis_results = transcript_agent.analyse_transcript(interview.transcript)
    
    # Extract and store Q&A pairs
    qa_pairs = extract_qa_pairs(interview.transcript)
    
    # Store questions and answers in database
    for qa_pair in qa_pairs:
        question = Question(
            question=qa_pair["question"],
            answer=qa_pair["answer"],
            interview_id=interview_id
        )
        db.add(question)
    
    # Update interview with analysis results
    interview.evaluation = analysis_results
    
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error storing analysis results: {str(e)}")
    
    return {
        "analysis": analysis_results,
        "questions_count": len(qa_pairs)
    } 