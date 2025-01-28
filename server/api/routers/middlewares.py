from fastapi import Request

from ..bll import service
from ..bll.base import async_session
from ..responses import bad_response
from ..settings import app


@app.middleware("http")
async def check_user_middleware(request: Request, call_next):
    """
    Middleware for checking user
    """

    if request.url.path.startswith("/api") and not request.url.path.startswith(
            "/api/medias/"
    ):
        async with async_session() as session:
            user = await service.get_has_user_by_api_key(
                session=session, api_key=request.headers.get("Api-Key")
            )
            if not user:
                return bad_response(
                    error_type="NotFound", error_message="User not found"
                )

    return await call_next(request)
