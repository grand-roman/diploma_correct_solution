from typing import List

from fastapi import UploadFile
from pydantic import BaseModel

from .base import GoodOut


class Author(BaseModel):
    id: int
    name: str


class Like(BaseModel):
    user_id: int
    name: str


class Tweet(BaseModel):
    id: int
    content: str
    attachments: List[str]
    author: Author
    likes: List[Like]


class TweetIn(BaseModel):
    tweet_data: str
    tweet_media_ids: List[int]


class TweetOut(GoodOut):
    tweet_id: int


class TweetFullOut(GoodOut):
    tweets: List[Tweet]


class MediaIn(BaseModel):
    file: UploadFile


class MediaOut(GoodOut):
    media_id: int
