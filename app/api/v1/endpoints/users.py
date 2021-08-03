from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import dtos
from app import repository
from app.api import deps


router = APIRouter()


@router.get("/", response_model=List[dtos.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    users = repository.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=dtos.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: dtos.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = repository.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = repository.user.create(db, obj_in=user_in)
    return user


@router.patch("/{username}/followers", response_model=dtos.User)
def add_user_follower(
    username: str, *, db: Session = Depends(deps.get_db), user_in: dtos.UserAddFollower
) -> Any:
    """
    Add follower to user.
    """
    user = repository.user.get_by_username(db, username=username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username not found!",
        )
    user = repository.user.add_follower(db, user=user, obj_in=user_in)
    return user


@router.delete("/{username}/followers", response_model=dtos.User)
def remove_user_follower(
    username: str,
    *,
    db: Session = Depends(deps.get_db),
    user_in: dtos.UserRemoveFollower,
) -> Any:
    """
    Remove follower from user (Unfollow).
    """
    user = repository.user.get_by_username(db, username=username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username not found!",
        )
    user = repository.user.remove_follower(db, user=user, obj_in=user_in)
    return user
