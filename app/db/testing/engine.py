from app.api.core.env_manager import EnvManager
from app.db import Base
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker



class TestingManager:
    engine = create_engine(EnvManager.TESTING_DB_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = Base

    @classmethod
    def get_db(cls):
        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")

        db = cls.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @classmethod
    def create_db(cls):
        cls.Base.metadata.create_all(cls.engine)
