"""Database connection and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

from src.config import settings

engine = create_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Must be sqlmodel.Session (not sqlalchemy.orm.Session): routes.py calls
# db.exec(...), which only exists on SQLModel's Session subclass. Using the
# plain SQLAlchemy Session here silently breaks every route that depends
# on get_db() (e.g. /tickets, /audit) with
# "AttributeError: 'Session' object has no attribute 'exec'".
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


def get_db() -> Session:
    """Yield a database session and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
