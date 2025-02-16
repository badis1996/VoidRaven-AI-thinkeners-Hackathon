import pytest
import base64
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate import Candidate
from app.models.interview import Interview

def get_test_cv_base64():
    """Get the test CV file as base64 encoded string."""
    cv_path = Path(__file__).parent / "cvexamples" / "Madrid-Resume-Template-Modern.pdf"
    with open(cv_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

@pytest.mark.asyncio
async def test_create_candidate(client: TestClient, db_session: AsyncSession):
    """Test creating a candidate with CV."""
    # Prepare test data
    test_data = {
        "name": "Test Candidate",
        "email": "test@example.com",
        "cv_file": get_test_cv_base64()
    }

    # Make request
    response = client.post("/api/v1/candidates/", json=test_data)
    
    # Check response
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == test_data["name"]
    assert data["email"] == test_data["email"]
    assert "cv_data" in data
    assert data["cv_data"]["mime_type"] == "application/pdf"

@pytest.mark.asyncio
async def test_create_duplicate_candidate(client: TestClient, db_session: AsyncSession):
    """Test creating a candidate with existing email."""
    # Create first candidate
    test_data = {
        "name": "Test Candidate",
        "email": "duplicate@example.com",
        "cv_file": get_test_cv_base64()
    }
    client.post("/api/v1/candidates/", json=test_data)

    # Try to create duplicate
    response = client.post("/api/v1/candidates/", json=test_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_update_interview_data(client: TestClient, db_session: AsyncSession):
    """Test updating interview data."""
    # First create a candidate
    candidate_data = {
        "name": "Interview Test",
        "email": "interview@example.com",
        "cv_file": get_test_cv_base64()
    }
    client.post("/api/v1/candidates/", json=candidate_data)

    # Update interview data
    interview_data = {
        "email": "interview@example.com",
        "audio_url": "https://example.com/audio.mp3",
        "transcript": "This is a test transcript"
    }
    response = client.post("/api/v1/candidates/interview", json=interview_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Interview data updated successfully"

@pytest.mark.asyncio
async def test_get_transcript(client: TestClient, db_session: AsyncSession):
    """Test getting interview transcript."""
    # First create a candidate
    candidate_data = {
        "name": "Transcript Test",
        "email": "transcript@example.com",
        "cv_file": get_test_cv_base64()
    }
    client.post("/api/v1/candidates/", json=candidate_data)

    # Add interview data
    interview_data = {
        "email": "transcript@example.com",
        "audio_url": "https://example.com/audio.mp3",
        "transcript": "Test transcript for retrieval"
    }
    client.post("/api/v1/candidates/interview", json=interview_data)

    # Get transcript
    response = client.get("/api/v1/candidates/transcript/transcript@example.com")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "transcript@example.com"
    assert data["transcript"] == "Test transcript for retrieval"
    assert "created_at" in data

@pytest.mark.asyncio
async def test_get_nonexistent_transcript(client: TestClient, db_session: AsyncSession):
    """Test getting transcript for non-existent candidate."""
    response = client.get("/api/v1/candidates/transcript/nonexistent@example.com")
    assert response.status_code == 404
    assert "No interview found" in response.json()["detail"] 