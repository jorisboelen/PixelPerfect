from fastapi import APIRouter
from pixelperfect.api.endpoints import albums, health, login, photos, users

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(login.router)
api_router.include_router(albums.router, prefix="/albums")
api_router.include_router(photos.router, prefix="/photos")
api_router.include_router(users.router, prefix="/users")
