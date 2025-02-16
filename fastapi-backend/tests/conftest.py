import asyncio
import pytest
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, drop_db_and_tables, create_db_and_tables

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
async def setup_db():
    """Reset database before each test."""
    await drop_db_and_tables()
    await create_db_and_tables()
    yield
    await drop_db_and_tables()

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a clean database session for each test."""
    async with AsyncSessionLocal() as session:
        # Start a transaction
        await session.begin()
        try:
            yield session
        finally:
            # Always rollback the transaction after the test
            await session.rollback()
            await session.close() 