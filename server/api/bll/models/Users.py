from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Base


class Followers(Base):
    __tablename__ = "followers"

    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    follower = relationship(
        "Users", back_populates="followers", foreign_keys=[follower_id]
    )
    following_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    following = relationship(
        "Users", back_populates="following", foreign_keys=[following_id]
    )


class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="likes")
    tweet_id = Column(Integer, ForeignKey("tweets.id"))
    tweet = relationship("Tweets", back_populates="likes")


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    api_key = Column(String(500), nullable=False)
    followers = relationship(
        "Followers",
        lazy="joined",
        back_populates="follower",
        cascade="all, delete-orphan",
        foreign_keys=[Followers.follower_id],
    )
    following = relationship(
        "Followers",
        lazy="joined",
        back_populates="following",
        cascade="all, delete-orphan",
        foreign_keys=[Followers.following_id],
    )
    tweets = relationship(
        "Tweets", lazy="joined", back_populates="author", cascade="all, delete-orphan"
    )
    likes = relationship(
        "Likes", lazy="joined", back_populates="user", cascade="all, delete-orphan"
    )
