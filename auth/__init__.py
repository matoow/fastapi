from fastapi import APIRouter, Cookie, Response
from starlette.responses import RedirectResponse

from auth import github
from logger import getLogger
from settings import settings
import jwt

api_router = APIRouter(
    prefix='/auth'
)
api_router.include_router(github.api_router)

logger = getLogger('auth')


@api_router.get("/check")
async def check(
    session: str = Cookie(default=None),
):
    try:
        user = jwt.decode(
            session,
            settings.secret,
            algorithms=['HS256'],
        )

        logger.debug('user: %s', user)
        return user

    except:
        return None


@api_router.get("/logout")
async def logout(response: Response):

    response.delete_cookie(key="session")

    return "OK"
