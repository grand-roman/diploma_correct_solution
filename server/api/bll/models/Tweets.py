from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.orm import relationship

from ..base import Base


class Tweets(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("Users", back_populates="tweets")
    attachments = relationship(
        "Medias", lazy="joined", back_populates="tweet", cascade="all, delete-orphan"
    )
    likes = relationship(
        "Likes", lazy="joined", back_populates="tweet", cascade="all, delete-orphan"
    )


class Medias(Base):
    __tablename__ = "medias"

    id = Column(Integer, primary_key=True)
    file_body = Column(LargeBinary)
    file_name = Column(String)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=True)
    tweet = relationship("Tweets", back_populates="attachments")
