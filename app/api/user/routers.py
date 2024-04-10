from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter, status
from .schemas import UserBase, UserCreate
from sqlalchemy.orm import Session
from app.db.postgres.engine import PostgresqlManager
from app.api.user import crud_user
from app.models.models import User
from app.api.login import get_current_active_user
from app.api.core.exceptions import ExistingValueError

router = APIRouter()
validate_user = Annotated[User, Depends(get_current_active_user)]



@router.post("/create", response_model=UserBase)
async def create_user(
    create_user: UserCreate, db: Session = Depends(PostgresqlManager.get_db)
):
    try:
        user = crud_user.create(db, create_user)
        return user
    except ExistingValueError as e:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{e}",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{e}",
                headers={"WWW-Authenticate": "Bearer"},
            )

@router.get("/{username}", response_model=UserBase)
async def get_user(username: str, current_user: validate_user, db: Session = Depends(PostgresqlManager.get_db)):
    user = crud_user.get_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username not exists in the system.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user