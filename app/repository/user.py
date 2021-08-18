from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi import status, HTTPException

from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

from app.repository.base import CreateSchemaType, ModelType, RepositoryBase
from app.models.user import User, follows


class RepositoryUser(RepositoryBase[User]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_following_by_user_id(self, db: Session, *, user_id: int) -> List[int]:
        """
        Get list following user
        """
        following = db.execute(
            follows.select(text(f"followee_id = {user_id}"))
        ).fetchall()
        followings = following[0] if len(following) > 0 else ()
        return followings

    def add_follower(
        self, db: Session, *, user: User, obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        data = {**obj_in_data, "followee_id": user.id}

        if data.get("follower_id") == user.id:
            raise HTTPException(status_code=400, detail="Can't follow your self!")

        try:
            stmt = follows.insert().values(**data)
            db.execute(stmt)
            db.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already follow the user!.",
            )
        return user

    def remove_follower(
        self, db: Session, *, user: User, obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        data = {**obj_in_data, "followee_id": user.id}

        if data.get("follower_id") == user.id:
            raise HTTPException(status_code=400, detail="Can't unfollow your self!")

        try:
            db.query(follows).filter_by(**data).delete()
            db.commit()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to proccess action!",
            )
        return user


user = RepositoryUser(User)
