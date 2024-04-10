from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool = True


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    email: str
    password: str
    verify_password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Additional properties stored in DB
class UserInDB(UserBase):
    hashed_password: str


class UserOut(BaseModel):
    pass
