import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.user.schemas import UserInDB, UserCreate, UserUpdate, UserBase
from app.api.core.security import get_password_hash
from app.api.crud.base import CRUDBase
from app.models.models import User
from app.api.core.exceptions import ExistingValueError

logger = logging.getLogger(__name__)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def create(self, db: Session, user_data: UserCreate) -> UserBase:
        try:
            hashed_password = get_password_hash(user_data.password)
            new_user = User(username=user_data.username,
                            hashed_password=hashed_password, email=user_data.email)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return new_user
        except IntegrityError as e:
            db.rollback()
            msg = "This username or email already exists in the system."
            logger.exception(f"Error creating user: {msg}")
            raise ExistingValueError(f"Error creating user: {msg}")
        except Exception as e:
            db.rollback()
            logger.exception(f"Error creating user: {str(e)}")
            raise ValueError(f"Error creating user: {str(e)}")

    def get_by_username(self, db: Session, username: str):
        try:
            user = db.query(User).filter_by(username=username).first()
            if user:
                return UserInDB(
                    username=user.username,
                    email=user.email,
                    is_active=user.is_active,
                    hashed_password=user.hashed_password,
                )
            return None
        except Exception as e:
            logger.exception(f"Error getting user by username: {str(e)}")
            raise ValueError(f"Error getting user by username: {str(e)}")


class SingletonCRUDUser:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonCRUDUser, cls).__new__(cls)
            cls._instance.crud_user = CRUDUser(User)
        return cls._instance.crud_user


crud_user = SingletonCRUDUser()
