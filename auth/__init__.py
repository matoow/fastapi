from fastapi import APIRouter
from auth import github

api_router = APIRouter(
  prefix='/auth'
)
api_router.include_router(github.api_router)
