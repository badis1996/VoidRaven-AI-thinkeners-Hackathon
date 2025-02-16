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
    await db_session.flush()
    
    # Verify the candidate was created
    result = await db_session.execute(select(Candidate).where(Candidate.email == "test@example.com"))
    db_candidate = result.scalar_one()
    
    assert db_candidate.id == candidate.id
    assert db_candidate.name == "Test Candidate"
    assert db_candidate.email == "test@example.com"
    assert db_candidate.cv_data == {"education": "Master's in Computer Science"}

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
    await db_session.flush()
    
    # Create an interview
    interview = Interview(
        id=uuid.uuid4(),
        candidate_id=candidate.id,
        transcript="Test interview transcript"
    )
    db_session.add(interview)
    await db_session.flush()
    
    # Create some questions
    questions = [
        Question(
            id=uuid.uuid4(),
            interview_id=interview.id,
            content="What is your experience with Python?",
            answer="I have 5 years of experience."
        ),
        Question(
            id=uuid.uuid4(),
            interview_id=interview.id,
            content="Tell me about your biggest project.",
            answer="I led a team of 5 developers."
        )
    ]
    for question in questions:
        db_session.add(question)
    await db_session.flush()
    
    # Verify everything was created correctly
    result = await db_session.execute(
        select(Interview).where(Interview.candidate_id == candidate.id)
    )
    db_interview = result.scalar_one()
    
    result = await db_session.execute(
        select(Question).where(Question.interview_id == interview.id)
    )
    db_questions = result.scalars().all()
    
    assert db_interview.transcript == "Test interview transcript"
    assert len(db_questions) == 2
    assert db_questions[0].content == "What is your experience with Python?"
    assert db_questions[1].content == "Tell me about your biggest project."

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
    await db_session.flush()
    
    # Create an interview with questions
    interview = Interview(
        id=uuid.uuid4(),
        candidate_id=candidate.id,
        transcript="Test cascade transcript"
    )
    db_session.add(interview)
    await db_session.flush()
    
    questions = [
        Question(
            id=uuid.uuid4(),
            interview_id=interview.id,
            content="First cascade question?",
            answer="First cascade answer"
        ),
        Question(
            id=uuid.uuid4(),
            interview_id=interview.id,
            content="Second cascade question?",
            answer="Second cascade answer"
        )
    ]
    for question in questions:
        db_session.add(question)
    await db_session.flush()
    
    # Delete the candidate
    await db_session.delete(candidate)
    await db_session.flush()
    
    # Verify cascade deletion
    result = await db_session.execute(
        select(Candidate).where(Candidate.id == candidate.id)
    )
    assert result.scalar_one_or_none() is None
    
    result = await db_session.execute(
        select(Interview).where(Interview.id == interview.id)
    )
    assert result.scalar_one_or_none() is None
    
    result = await db_session.execute(
        select(Question).where(Question.interview_id == interview.id)
    )
    assert len(result.scalars().all()) == 0 