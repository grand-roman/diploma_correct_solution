from fastapi import Depends, Header, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from ..bll import service
from ..bll.base import get_session
from ..responses import bad_response, tweets_response
from ..schemas import (ErrorOut, GoodOut, MediaOut, TweetFullOut, TweetIn, TweetOut)
from ..settings import app


@app.get(
    "/api/medias/{media_id}",
    response_class=Response,
    responses={404: {"model": ErrorOut}},
)
async def get_media(
        media_id: int, session: AsyncSession = Depends(get_session)
) -> Response:
    """
    Response image
    """

    media = await service.get_media_by_id(session, media_id)

    if not media:
        return bad_response("NotFound", "Media not found")

    return Response(content=media.file_body, media_type="image/png")


@app.post(
    "/api/medias",
    response_model=MediaOut,
    responses={404: {"model": ErrorOut}},
)
async def create_media(
        file: UploadFile,
        api_key: str = Header(),
        session: AsyncSession = Depends(get_session),
) -> MediaOut:
    """
    Add new image
    """

    file_body = await file.read()
    media = await service.create_media(
        session, file_name=file.filename, file_body=file_body
    )

    return MediaOut(media_id=media.id)


@app.get(
    "/api/tweets",
    response_model=TweetFullOut,
    responses={404: {"model": ErrorOut}},
)
async def get_tweets(
        api_key: str = Header(), session: AsyncSession = Depends(get_session)
) -> TweetFullOut:
    """
    Get tweets
    """

    user = await service.get_user_by_api_key(session, api_key)

    author_ids = [i_follow.follower_id for i_follow in user.following]
    author_ids.append(user.id)

    tweets = await service.get_tweets(session, author_ids)

    return tweets_response(tweets)


@app.post(
    "/api/tweets",
    response_model=TweetOut,
    responses={404: {"model": ErrorOut}},
)
async def create_tweet(
        tweet_data: TweetIn,
        api_key: str = Header(),
        session: AsyncSession = Depends(get_session),
) -> TweetOut:
    """
    Add new tweet
    """

    user = await service.get_user_by_api_key(session, api_key)
    tweet = await service.create_tweet(
        session,
        content=tweet_data.tweet_data,
        author_id=user.id,
        media_ids=tweet_data.tweet_media_ids,
    )

    return TweetOut(tweet_id=tweet.id)


@app.delete(
    "/api/tweets/{tweet_id}",
    response_model=GoodOut,
    responses={404: {"model": ErrorOut}},
)
async def delete_tweet(
        tweet_id: int, api_key: str = Header(), session: AsyncSession = Depends(get_session)
) -> GoodOut:
    """
    Delete tweet
    """

    await service.remove_tweet(session, tweet_id)

    return GoodOut()


@app.post(
    "/api/tweets/{tweet_id}/likes",
    response_model=GoodOut,
    responses={404: {"model": ErrorOut}},
)
async def like_tweet(
        tweet_id: int, api_key: str = Header(), session: AsyncSession = Depends(get_session)
) -> GoodOut:
    """
    Add like to tweet
    """

    user = await service.get_user_by_api_key(session, api_key)
    await service.like_tweet(session, tweet_id, user.id)

    return GoodOut()


@app.delete(
    "/api/tweets/{tweet_id}/likes",
    response_model=GoodOut,
    responses={404: {"model": ErrorOut}},
)
async def remove_like_tweet(
        tweet_id: int, api_key: str = Header(), session: AsyncSession = Depends(get_session)
) -> GoodOut:
    """
    Delete like from tweet
    """

    user = await service.get_user_by_api_key(session, api_key)
    await service.remove_like(session, tweet_id, user.id)

    return GoodOut()
