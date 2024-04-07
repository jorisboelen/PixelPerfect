from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from os import path

from pixelperfect import __application__, __version__
from pixelperfect.api.api import api_router
from pixelperfect.core.settings import settings
from pixelperfect.security.middleware import SessionCookieMiddleware


app = FastAPI(
    title=__application__,
    version=__version__,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url=None
)

app.add_middleware(SessionCookieMiddleware)
app.add_middleware(CORSMiddleware,
                   allow_origins=[str(origin) for origin in settings.CORS_ALLOWED_ORIGINS],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
app.include_router(api_router, prefix="/api")
app.mount("/", StaticFiles(directory=path.join(path.dirname(__file__), "static"), html=True), name="static")
