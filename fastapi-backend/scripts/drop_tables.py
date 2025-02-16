from sqlalchemy import create_engine
from app.core.config import settings
from app.models.base import Base

def drop_tables():
    engine = create_engine(settings.sync_database_url)
    Base.metadata.drop_all(engine)

if __name__ == "__main__":
    drop_tables()
    print("All tables dropped successfully") 