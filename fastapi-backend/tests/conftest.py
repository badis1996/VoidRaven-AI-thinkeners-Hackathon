import asyncio
import pytest
from typing import AsyncGenerator, Generator

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.database import get_db
from app.main import app
from app.models.base import Base

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine(event_loop):
    """Create test engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
        echo=False,
    )
    yield engine
    await engine.dispose()

@pytest.fixture(scope="session")
async def test_async_session(test_engine):
    """Create test async session factory."""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    yield async_session

@pytest.fixture(autouse=True)
async def test_db(test_engine):
    """Create test database."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(test_async_session) -> AsyncGenerator[AsyncSession, None]:
    """Create a clean database session for each test."""
    async with test_async_session() as session:
        try:
            yield session
        finally:
            await session.close()

@pytest.fixture
def client(db_session: AsyncSession) -> Generator:
    """Create a test client with the test database."""
    async def override_get_db():
        try:
            yield db_session
        finally:
            await db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    del app.dependency_overrides[get_db] 