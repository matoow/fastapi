from fastapi import APIRouter, HTTPException, Response
from starlette.requests import Request
from fastapi_sso.sso.github import GithubSSO
import jwt
from logger import getLogger

from settings import settings

logger = getLogger()

gh_sso = GithubSSO(
    settings.gh_client_id,
    settings.gh_client_secret,
    settings.gh_callback_url
)

api_router = APIRouter(
    prefix='/github'
)


@api_router.get("/")
async def root():
    logger.debug("Hello auth")
    return {"message": "Hello auth"}


@api_router.get("/login")
async def gh_login():
    return await gh_sso.get_login_redirect()


@api_router.get("/callback")
async def gh_callback(request: Request, response: Response):
    user = await gh_sso.verify_and_process(request)

    if user is None:
        raise HTTPException(401, "Failed to fetch user information")

    payload = {
        "id": user.id,
        "picture": user.picture,
        "display_name": user.display_name,
        "email": user.email,
        "provider": user.provider,
    }

    encoded_jwt = jwt.encode(
        payload,
        settings.secret,
        algorithm='HS256',
    )

    response.set_cookie(key="session", value=encoded_jwt)

    return payload
