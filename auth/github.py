from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from fastapi_sso.sso.github import GithubSSO

from settings import settings


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
    return {"message": "Hello auth"}


@api_router.get("/login")
async def gh_login():
    return await gh_sso.get_login_redirect()


@api_router.get("/callback")
async def gh_callback(request: Request):
    user = await gh_sso.verify_and_process(request)

    if user is None:
        raise HTTPException(401, "Failed to fetch user information")

    return {
        "id": user.id,
        "picture": user.picture,
        "display_name": user.display_name,
        "email": user.email,
        "provider": user.provider,
        "app_name": settings.app_name,
    }
