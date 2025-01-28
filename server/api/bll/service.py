from typing import List

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Followers, Likes, Medias, Tweets, Users


async def get_has_user_by_api_key(session: AsyncSession, api_key: str) -> bool:
    result = await session.execute(select(Users.id).where(Users.api_key == api_key))
    return result.scalars().first() is not None


async def get_user_by_api_key(session: AsyncSession, api_key: str) -> Users:
    result = await session.execute(select(Users).where(Users.api_key == api_key))
    return result.scalars().first()


async def get_user_by_id(session: AsyncSession, user_id: int) -> Users:
    result = await session.execute(select(Users).where(Users.id == user_id))
    return result.scalars().first()


async def create_user(session: AsyncSession, name: str, api_key: str) -> Users:
    new_user = Users(name=name, api_key=api_key)
    new_user.following = []
    new_user.followers = []
    new_user.tweets = []
    new_user.likes = []

    session.add(new_user)
    await session.commit()

    return new_user


async def follow(session: AsyncSession, follower_id: int, following_id: int) -> None:
    session.add(Followers(follower_id=follower_id, following_id=following_id))
    await session.commit()


async def remove_follow(
    session: AsyncSession, follower_id: int, following_id: int
) -> None:
    await session.execute(
        delete(Followers).where(
            Followers.follower_id == follower_id, Followers.following_id == following_id
        )
    )
    await session.commit()


async def get_media_by_id(session: AsyncSession, media_id: int) -> Medias:
    result = await session.execute(select(Medias).where(Medias.id == media_id))
    return result.scalars().first()


async def create_media(
    session: AsyncSession, file_name: str, file_body: bytes
) -> Medias:
    new_media = Medias(file_name=file_name, file_body=file_body)

    session.add(new_media)
    await session.commit()

    return new_media


async def get_tweets(session: AsyncSession, author_ids: List[int]) -> List[Tweets]:
    result = await session.execute(
        select(Tweets).where(Tweets.author_id.in_(author_ids))
    )
    tweets = result.unique().scalars().all()

    for i_tweet in tweets:
        i_tweet.author = await get_user_by_id(session, i_tweet.author_id)

    return tweets


async def create_tweet(
    session: AsyncSession, content: str, author_id: int, media_ids: List[int]
) -> Medias:
    new_tweet = Tweets(content=content, author_id=author_id)

    session.add(new_tweet)
    await session.commit()

    for i_media_id in media_ids:
        media = await get_media_by_id(session, i_media_id)
        media.tweet_id = new_tweet.id

    await session.commit()

    return new_tweet


async def remove_tweet(session: AsyncSession, tweet_id: int) -> Medias:
    await session.execute(delete(Likes).where(Likes.tweet_id == tweet_id))
    await session.execute(delete(Medias).where(Medias.tweet_id == tweet_id))
    await session.execute(delete(Tweets).where(Tweets.id == tweet_id))
    await session.commit()


async def like_tweet(session: AsyncSession, tweet_id: int, user_id: int) -> Medias:
    new_like = Likes(user_id=user_id, tweet_id=tweet_id)

    session.add(new_like)
    await session.commit()

    return new_like


async def remove_like(session: AsyncSession, tweet_id: int, user_id: int) -> Medias:
    await session.execute(
        delete(Likes).where(Likes.tweet_id == tweet_id, Likes.user_id == user_id)
    )
    await session.commit()
