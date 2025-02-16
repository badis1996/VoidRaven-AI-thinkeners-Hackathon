import asyncio
import base64
from pathlib import Path

from sqlalchemy.future import select
from app.core.database import AsyncSessionLocal
from app.models.candidate import Candidate

async def add_example_cv():
    """Add example CV to the database."""
    # Read and encode the CV file
    cv_path = Path(__file__).parent.parent / "tests" / "cvexamples" / "Madrid-Resume-Template-Modern.pdf"
    with open(cv_path, "rb") as f:
        cv_content = base64.b64encode(f.read()).decode()

    async with AsyncSessionLocal() as session:
        # Check if example candidate exists
        result = await session.execute(
            select(Candidate).where(Candidate.email == "example@voidraven.ai")
        )
        if result.scalar_one_or_none():
            print("Example candidate already exists")
            return

        # Create example candidate
        candidate = Candidate(
            name="Example Candidate",
            email="example@voidraven.ai",
            cv_data={
                "pdf_content": cv_content,
                "mime_type": "application/pdf"
            }
        )
        session.add(candidate)
        await session.commit()
        print("Example CV added successfully")

if __name__ == "__main__":
    asyncio.run(add_example_cv()) 