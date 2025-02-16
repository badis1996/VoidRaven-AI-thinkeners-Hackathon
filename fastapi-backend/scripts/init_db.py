import asyncio
import logging
from sqlalchemy.exc import ProgrammingError
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from app.core.config import settings
from app.core.database import create_db_and_tables

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_database() -> None:
    """Create database if it doesn't exist."""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=settings.POSTGRES_HOSTNAME,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(
            f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{settings.POSTGRES_DB}'"
        )
        exists = cursor.fetchone()
        
        if not exists:
            # Create database
            cursor.execute(f'CREATE DATABASE "{settings.POSTGRES_DB}"')
            logger.info(f"Created database {settings.POSTGRES_DB}")
        else:
            logger.info(f"Database {settings.POSTGRES_DB} already exists")

        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise

async def init_db() -> None:
    """Initialize database with tables."""
    try:
        await create_database()
        await create_db_and_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(init_db()) 