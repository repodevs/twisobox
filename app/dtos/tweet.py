from typing import Optional

from pydantic import BaseModel


# Shared properties
class TweetBase(BaseModel):
    sender_id: int
    text: str


class TweetCreate(BaseModel):
    sender_id: int
    text: str


class TweetInDBBase(TweetBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Response
class Tweet(TweetInDBBase):
    pass
