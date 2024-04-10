from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.api.core.env_manager import EnvManager

# Create a SQLAlchemy engine using the database URL from the environment manager
engine = create_engine(
    EnvManager.SQLALCHEMY_DATABASE_URL
)

class PostgresqlManager:
    """
    PostgresqlManager is a class that manages the database connection and session.

    It provides a session for database operations and ensures that the session is properly
    closed after its use.

    Usage:
        Use the `get_db` class method as a dependency in FastAPI route functions to obtain
        a database session.

    Attributes:
        SessionLocal (sqlalchemy.orm.session.Session): A SQLAlchemy session factory.
        Base (sqlalchemy.ext.declarative.api.Base): The SQLAlchemy Base class for declarative models.

    Methods:
        get_db(): A class method that yields a database session for route function dependencies.

    """
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = Base

    @classmethod
    def get_db(cls):
        db = cls.SessionLocal()
        try:
            yield db
        finally:
            db.close()
