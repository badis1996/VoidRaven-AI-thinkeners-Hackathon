import asyncio
import pytest
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.candidate import Candidate
from app.models.interview import Interview
from app.models.question import Question

@pytest.mark.asyncio
async def test_create_candidate(db_session: AsyncSession):
    """Test creating a candidate."""
    # Create a test candidate
    candidate = Candidate(
        id=uuid.uuid4(),
        name="Test Candidate",
        email="test@example.com",
        cv_data={"education": "Master's in Computer Science"}
    )
    
    db_session.add(candidate)
    await db_session.commit()
    await db_session.refresh(candidate)
    
    # Verify the candidate was created
    assert candidate.id is not None
    assert candidate.name == "Test Candidate"
    assert candidate.email == "test@example.com"
    assert candidate.cv_data == {"education": "Master's in Computer Science"}

@pytest.mark.asyncio
async def test_create_interview_with_questions(db_session: AsyncSession):
    """Test creating an interview with questions."""
    # Create a candidate first
    candidate = Candidate(
        id=uuid.uuid4(),
        name="Interview Test Candidate",
        email="interview.test@example.com"
    )
    db_session.add(candidate)
    await db_session.commit()
    
    # Create an interview
    interview = Interview(
        id=uuid.uuid4(),
        candidate_id=candidate.id,
        transcript="Test interview transcript"
    )
    db_session.add(interview)
    await db_session.commit()
    
    # Add some questions
    questions = [
        Question(
            id=uuid.uuid4(),
            interview_id=interview.id,
            question="What is your background?",
            answer="I have a degree in Computer Science"
        ),
        Question(
            id=uuid.uuid4(),
            interview_id=interview.id,
            question="Why do you want to join this program?",
            answer="To enhance my knowledge in AI"
        )
    ]
    
    db_session.add_all(questions)
    await db_session.commit()
    
    # Verify the interview and questions were created
    stmt = select(Interview).where(Interview.id == interview.id)
    result = await db_session.execute(stmt)
    saved_interview = result.scalar_one()
    
    assert saved_interview.id == interview.id
    assert saved_interview.candidate_id == candidate.id
    assert saved_interview.transcript == "Test interview transcript"
    
    # Verify questions
    stmt = select(Question).where(Question.interview_id == interview.id)
    result = await db_session.execute(stmt)
    saved_questions = result.scalars().all()
    
    assert len(saved_questions) == 2
    assert all(q.interview_id == interview.id for q in saved_questions)

@pytest.mark.asyncio
async def test_cascade_delete(db_session: AsyncSession):
    """Test that deleting a candidate cascades to interviews and questions."""
    # Create a candidate
    candidate = Candidate(
        id=uuid.uuid4(),
        name="Cascade Test Candidate",
        email="cascade.test@example.com"
    )
    db_session.add(candidate)
    await db_session.commit()
    
    # Create an interview
    interview = Interview(
        id=uuid.uuid4(),
        candidate_id=candidate.id
    )
    db_session.add(interview)
    await db_session.commit()
    
    # Add a question
    question = Question(
        id=uuid.uuid4(),
        interview_id=interview.id,
        question="Test question?",
        answer="Test answer"
    )
    db_session.add(question)
    await db_session.commit()
    
    # Delete the candidate
    await db_session.delete(candidate)
    await db_session.commit()
    
    # Verify cascade delete
    stmt = select(Interview).where(Interview.id == interview.id)
    result = await db_session.execute(stmt)
    deleted_interview = result.scalar_one_or_none()
    assert deleted_interview is None
    
    stmt = select(Question).where(Question.id == question.id)
    result = await db_session.execute(stmt)
    deleted_question = result.scalar_one_or_none()
    assert deleted_question is None 