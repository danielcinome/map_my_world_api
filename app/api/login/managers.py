from jose import JWTError, jwt
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.postgres.engine import PostgresqlManager
from app.api.core.security import verify_password
from app.api.core.env_manager import EnvManager
from app.models.models import User
from app.api.user import crud_user
from .schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/access-token")


def authenticate_user(db: Session, username: str, password: str):
    user = crud_user.get_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(PostgresqlManager.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, EnvManager.SECRET_KEY,
                             algorithms=[EnvManager.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud_user.get_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
