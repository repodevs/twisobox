from typing import Any
from sqlalchemy.orm.session import Session
from fastapi import APIRouter, Depends, HTTPException
from app import repository
from app.api import deps

router = APIRouter()


@router.get("/{username}")
def read_timeline_user(
    username: str, db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 10
) -> Any:
    """
    Read timelines by user username.
    """
    user = repository.user.get_by_username(db, username=username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username `{username}` not found!"
        )
    timelines = repository.timeline.get_by_sender_id(
        db, sender_id=user.id, skip=skip, limit=limit
    )
    return timelines
