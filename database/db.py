"""
Crown of Kaliyug — Database Connection
Phase 0: Foundation
"""
import os
import sys
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from loguru import logger

# Add project root to sys.path for direct script execution
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./crown_of_kaliyug.db"  # Zero-Docker Fallback
)

engine_args = {
    "pool_pre_ping": True,
}
if not DATABASE_URL.startswith("sqlite"):
    engine_args["pool_size"] = 10
    engine_args["max_overflow"] = 20

engine = create_engine(DATABASE_URL, **engine_args, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db() -> Session:
    """Context manager for database sessions."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"DB session error: {e}")
        raise
    finally:
        db.close()


def init_db():
    """Create all tables. Run once on setup."""
    from database.models import Base
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created.")


if __name__ == "__main__":
    init_db()