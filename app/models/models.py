from app.db.postgres.engine import PostgresqlManager
from sqlalchemy import Column, DateTime, String, Boolean, ForeignKey, Float
from datetime import datetime
import uuid
from app.db.utils.dialect_translator import GUID, CustomDateTime


class ChangesTracking(PostgresqlManager.Base):
    __abstract__ = True

    created_on = Column(DateTime(), default=datetime.utcnow)
    updated_on = Column(DateTime(), default=datetime.utcnow,
                        onupdate=datetime.utcnow)


class User(ChangesTracking):
    __tablename__ = 'user'

    uuid = Column(GUID(), primary_key=True, default=uuid.uuid4,
                  unique=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)

class Location(ChangesTracking):
    __tablename__ = 'location'

    uuid = Column(GUID(), primary_key=True, default=uuid.uuid4,
                  unique=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

class Category(ChangesTracking):
    __tablename__ = 'category'

    uuid = Column(GUID(), primary_key=True, default=uuid.uuid4,
                  unique=True, nullable=False)
    name = Column(String, nullable=False, unique=True)

class LocationCategoryReviewed(ChangesTracking):
    __tablename__ = 'location_category_reviewed'

    location_uuid = Column(GUID(), ForeignKey('location.uuid'), primary_key=True)
    category_uuid = Column(GUID(), ForeignKey('category.uuid'), primary_key=True)
    last_reviewed_date = Column(CustomDateTime())
