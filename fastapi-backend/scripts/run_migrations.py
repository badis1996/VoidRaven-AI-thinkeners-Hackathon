import logging
import os
import sys
from alembic.config import Config
from alembic import command

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations() -> None:
    """Run database migrations."""
    try:
        # Get the directory containing this script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Get the project root directory (parent of current directory)
        project_root = os.path.dirname(current_dir)
        
        # Create Alembic configuration
        alembic_cfg = Config(os.path.join(project_root, "alembic.ini"))
        alembic_cfg.set_main_option("script_location", os.path.join(project_root, "alembic"))
        
        # Run the migration
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed successfully")
        
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migrations() 