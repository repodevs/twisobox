from sqlalchemy import Column, ForeignKey, BigInteger, String, func, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.db.base_class import Base


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(BigInteger, primary_key=True, index=True)
    sender_id = Column(BigInteger, ForeignKey("users.id"))
    text = Column(String)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())


class Outbox(Base):
    __tablename__ = "tweets_outbox"

    event_id = Column(UUID, primary_key=True, server_default=func.uuid_generate_v4())
    aggregate_id = Column(Text)  # value is `aggregate_id` is from `tweets.id`
    type = Column(Text)
    aggregate = Column(JSONB)
    created_at = Column(TIMESTAMP, server_default=func.now())
