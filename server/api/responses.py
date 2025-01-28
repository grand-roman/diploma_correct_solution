from typing import List

from starlette.responses import JSONResponse

from . import schemas
from .bll import models


def bad_response(error_type: str, error_message: str) -> JSONResponse:
    """
    Return bad response
    """

    content = schemas.ErrorOut(
        error_type="UserNotFound", error_message="User not found"
    ).__dict__
    return JSONResponse(status_code=404, content=content)


def user_response(user: models.Users) -> schemas.UserOut:
    """
    Return User response
    """
    return schemas.UserOut(
        user=schemas.User(
            id=user.id,
            name=user.name,
            followers=[
                schemas.Follow(id=i_follow.follower.id, name=i_follow.follower.name)
                for i_follow in user.followers
            ],
            following=[
                schemas.Follow(id=i_follow.following.id, name=i_follow.following.name)
                for i_follow in user.following
            ],
        )
    )


def tweets_response(tweets: List[models.Tweets]) -> schemas.TweetFullOut:
    """
    Return Tweets response
    """
    return schemas.TweetFullOut(
        tweets=[
            schemas.Tweet(
                id=i_tweet.id,
                content=i_tweet.content,
                attachments=[
                    f"/api/medias/{i_attachment.id}"
                    for i_attachment in i_tweet.attachments
                ],
                author=schemas.Author(id=i_tweet.author.id, name=i_tweet.author.name),
                likes=[
                    schemas.Like(user_id=i_like.user.id, name=i_like.user.name)
                    for i_like in i_tweet.likes
                ],
            )
            for i_tweet in tweets
        ]
    )
