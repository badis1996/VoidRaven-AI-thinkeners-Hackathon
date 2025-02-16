import pytest
import base64
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.main import app
from app.models.candidate import Candidate
from app.models.interview import Interview
from tests.utils import get_test_cv_base64

@pytest.mark.asyncio
async def test_create_candidate(client, db_session: AsyncSession):
    """Test creating a candidate with CV."""
    # Prepare test data
    test_data = {
        "name": "Test Candidate",
        "email": "test@example.com",
        "cv_file": get_test_cv_base64()
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/candidates/", json=test_data)
        assert response.status_code == 201
        
        # Verify in database
        result = await db_session.execute(
            select(Candidate).where(Candidate.email == "test@example.com")
        )
        candidate = result.scalar_one()
        assert candidate.name == "Test Candidate"
        assert candidate.email == "test@example.com"

@pytest.mark.asyncio
async def test_create_duplicate_candidate(client, db_session: AsyncSession):
    """Test creating a candidate with existing email."""
    # Create first candidate
    test_data = {
        "name": "Test Candidate",
        "email": "duplicate@example.com",
        "cv_file": get_test_cv_base64()
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First creation should succeed
        response = await ac.post("/api/v1/candidates/", json=test_data)
        assert response.status_code == 201

        # Second creation should fail
        response = await ac.post("/api/v1/candidates/", json=test_data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_update_interview_data(client, db_session: AsyncSession):
    """Test updating interview data."""
    # First create a candidate
    candidate_data = {
        "name": "Interview Test",
        "email": "interview@example.com",
        "cv_file": get_test_cv_base64()
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create candidate
        response = await ac.post("/api/v1/candidates/", json=candidate_data)
        assert response.status_code == 201

        # Update interview data
        interview_data = {
            "email": "interview@example.com",
            "transcript": "Test interview transcript",
            "questions": [
                {
                    "content": "What is your experience?",
                    "answer": "5 years of experience"
                }
            ]
        }
        
        response = await ac.post("/api/v1/candidates/interview", json=interview_data)
        assert response.status_code == 200

        # Verify in database
        result = await db_session.execute(
            select(Interview)
            .join(Candidate)
            .where(Candidate.email == "interview@example.com")
            .options(selectinload(Interview.questions))
        )
        interview = result.scalar_one()
        assert interview.transcript == "Test interview transcript"
        assert len(interview.questions) == 1
        assert interview.questions[0].content == "What is your experience?"

@pytest.mark.asyncio
async def test_get_transcript(client, db_session: AsyncSession):
    """Test getting interview transcript."""
    # First create a candidate
    candidate_data = {
        "name": "Transcript Test",
        "email": "transcript@example.com",
        "cv_file": get_test_cv_base64()
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create candidate
        response = await ac.post("/api/v1/candidates/", json=candidate_data)
        assert response.status_code == 201

        # Add interview data
        interview_data = {
            "email": "transcript@example.com",
            "transcript": "Test transcript content",
            "questions": []
        }
        
        response = await ac.post("/api/v1/candidates/interview", json=interview_data)
        assert response.status_code == 200

        # Get transcript
        response = await ac.get(f"/api/v1/candidates/transcript/{candidate_data['email']}")
        assert response.status_code == 200
        assert response.json()["transcript"] == "Test transcript content"

@pytest.mark.asyncio
async def test_get_nonexistent_transcript(client, db_session: AsyncSession):
    """Test getting transcript for non-existent candidate."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/candidates/transcript/nonexistent@example.com")
        assert response.status_code == 404 