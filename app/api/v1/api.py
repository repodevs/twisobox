from fastapi import APIRouter

from app.api.v1.endpoints import timelines, tweets, users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tweets.router, prefix="/tweets", tags=["tweets"])
api_router.include_router(timelines.router, prefix="/timelines", tags=["timelines"])
