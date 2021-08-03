from typing import Optional

from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
    username: str
    is_active: Optional[bool] = True


class UserCreate(BaseModel):
    username: str


class UserUpdate(BaseModel):
    username: Optional[str] = None


class UserAddFollower(BaseModel):
    follower_id: int


class UserRemoveFollower(BaseModel):
    follower_id: int


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Response
class User(UserInDBBase):
    pass
