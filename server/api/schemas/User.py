from typing import List

from pydantic import BaseModel

from .base import GoodOut


class Follow(BaseModel):
    id: int
    name: str


class User(BaseModel):
    id: int
    name: str
    followers: List[Follow]
    following: List[Follow]


class UserOut(GoodOut):
    user: User


class UserIn(BaseModel):
    name: str
    api_key: str
