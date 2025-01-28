from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from ..bll import service
from ..bll.base import get_session
from ..responses import bad_response, user_response
from ..schemas import (ErrorOut, GoodOut, UserIn, UserOut)
from ..settings import app


@app.get(
    path="/api/users/me",
    response_model=UserOut,
    responses={404: {"model": ErrorOut}},
)
async def get_current_user(
        api_key: str = Header(), session: AsyncSession = Depends(get_session)
) -> UserOut:
    """
    Get current user
    """

    user = await service.get_user_by_api_key(session, api_key)
    return user_response(user)


@app.get(
    path="/api/users/{user_id}",
    response_model=UserOut,
    responses={404: {"model": ErrorOut}},
)
async def get_user_by_id(
        user_id: int, api_key: str = Header(), session: AsyncSession = Depends(get_session)
) -> UserOut:
    """
    Get user by id
    """

    user = await service.get_user_by_id(session, user_id)
    if not user:
        return bad_response(error_type="NotFound", error_message="User not found")

    return user_response(user)


@app.post(
    path="/users/add",
    response_model=UserOut,
    responses={404: {"model": ErrorOut}},
)
async def create_user(
        user_data: UserIn, session: AsyncSession = Depends(get_session)
) -> UserOut:
    """
    Create new user
    """

    user = await service.get_user_by_api_key(session, user_data.api_key)

    if not user:
        user = await service.create_user(
            session, name=user_data.name, api_key=user_data.api_key
        )

    return user_response(user)


@app.post(
    path="/api/users/{user_id}/follow",
    response_model=GoodOut,
    responses={404: {"model": ErrorOut}},
)
async def follow_user(
        user_id: int, api_key: str = Header(), session: AsyncSession = Depends(get_session)
) -> GoodOut:
    """
    Add follow to user
    """

    following_user = await service.get_user_by_api_key(session, api_key)
    follower_user = await service.get_user_by_id(session, user_id)

    if not follower_user:
        return bad_response("NotFound", "User not found")

    await service.follow(session, follower_user.id, following_user.id)

    return GoodOut()


@app.delete(
    "/api/users/{user_id}/follow",
    response_model=GoodOut,
    responses={404: {"model": ErrorOut}},
)
async def delete_follow_user(
        user_id: int, api_key: str = Header(), session: AsyncSession = Depends(get_session)
) -> GoodOut:
    """
    Delete follow to user
    """

    following_user = await service.get_user_by_api_key(session, api_key)
    follower_user = await service.get_user_by_id(session, user_id)

    if not follower_user:
        return bad_response("NotFound", "User not found")

    await service.remove_follow(session, follower_user.id, following_user.id)

    return GoodOut()
