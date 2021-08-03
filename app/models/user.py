from sqlalchemy import Boolean, Column, BigInteger, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# for many-to-many
follows = Table(
    "follows",
    Base.metadata,
    Column("followee_id", ForeignKey("users.id"), primary_key=True),
    Column("follower_id", ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    is_active = Column(Boolean, default=True, server_default="true")
    followers = relationship(
        "User",
        secondary=follows,
        primaryjoin=follows.c.followee_id == id,
        secondaryjoin=follows.c.follower_id == id,
        backref="followees",
    )
