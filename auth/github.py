from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from fastapi_sso.sso.github import GithubSSO

GH_CLIENT_ID = "Iv1.5977bf5d625594cd"
GH_CLIENT_SECRET = "e0505bfcd8553630377f4eedfe9b8a0a908bdc1e"
GH_CALLBACK_URL = "http://localhost:8000/auth/github/callback"


gh_sso = GithubSSO(GH_CLIENT_ID, GH_CLIENT_SECRET, GH_CALLBACK_URL)

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
    }
