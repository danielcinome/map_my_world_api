from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.postgres.engine import PostgresqlManager
from app.api.core.security import create_access_token
from .managers import authenticate_user
from .schemas import Token

router = APIRouter()


@router.post("/access-token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(PostgresqlManager.get_db)
):
    """
    Generate an access token.

    This endpoint allows the external user (API developer) to obtain an access token
    by providing valid user credentials.

    - The access token is necessary for making authenticated requests to protected
      endpoints.
    - The token has a limited lifespan determined by the server.

    Returns:
    - dict: A dictionary containing the generated access token and its type.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
