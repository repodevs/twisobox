from typing import List

from sqlalchemy.orm.session import Session

from app.repository.base import RepositoryBase
from app.models import Tweet, User

from .user import user as userRepo


class RepositoryTimeline(RepositoryBase[Tweet]):
    def get_by_sender_id(
        self, db: Session, *, sender_id: int, skip: int = 0, limit: int = 10
    ) -> List[Tweet]:
        """
        Get List tweet be sender_id.
        """
        tweets = (
            db.query(Tweet)
            .filter(Tweet.sender_id == sender_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return tweets

    def get_by_username(
        self, db: Session, *, user: User, skip: int = 0, limit: int = 10
    ) -> List[Tweet]:
        """
        Get List tweet from user following.
        """
        # List following user
        followings = userRepo.get_following_by_user_id(db, user_id=user.id)

        tweets = (
            db.query(Tweet)
            .filter(User.id.in_(followings))
            .order_by(Tweet.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return tweets


timeline = RepositoryTimeline(Tweet)
