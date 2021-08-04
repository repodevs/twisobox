from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from app.repository.base import CreateSchemaType, ModelType, RepositoryBase
from app.models.tweet import Tweet, Outbox


class RepositoryTweet(RepositoryBase[Tweet]):
    def publishTweet(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Save tweet to Tweets table and Outbox table.
        """
        # Save to Tweets table
        obj_in_data = jsonable_encoder(obj_in)
        data = {**obj_in_data}
        db_obj = self.model(**data)  # type: ignore
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)

        # Insert to Outbox table
        tweetData = jsonable_encoder(db_obj)
        tweetOutbox = Outbox(
            aggregate_id=db_obj.id, type="create_tweet", aggregate=tweetData
        )
        db.add(tweetOutbox)

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Failed to Post Tweets!.",
            )

        return db_obj


tweet = RepositoryTweet(Tweet)
