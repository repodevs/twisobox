from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app import dtos, repository
from app.api import deps


router = APIRouter()


@router.post("/", response_model=dtos.Tweet)
def create_tweet(
    *, db: Session = Depends(deps.get_db), tweet_in: dtos.TweetCreate
) -> Any:
    """
    Create new tweet.
    """
    tweet = repository.tweet.create(db, obj_in=tweet_in)
    return tweet
