from sqlalchemy import Column, ForeignKey, BigInteger, String, func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.db.base_class import Base


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(BigInteger, primary_key=True, index=True)
    sender_id = Column(BigInteger, ForeignKey("users.id"))
    text = Column(String)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())
