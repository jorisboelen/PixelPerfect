from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from pixelperfect.db import crud
from pixelperfect.db.database import get_db
from pixelperfect.db.models import UserSession


SESSION_TOKEN_LIST = {}
AUTH_INCLUDED_PREFIX = '/api/'
AUTH_EXCLUDED_URLS = ['/api/health', '/api/login', '/api/logout', '/api/docs', '/api/openapi.json']
ADMIN_METHODS = ['DELETE', 'PATCH', 'POST', 'PUT']


class SessionCookieMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(AUTH_INCLUDED_PREFIX) and request.url.path not in AUTH_EXCLUDED_URLS:
            session_token = request.cookies.get('session_token')
            if not session_token:
                return JSONResponse(status_code=403, content={"detail": "Not logged in"})
            elif session_token not in SESSION_TOKEN_LIST:
                return JSONResponse(status_code=403, content={"detail": "Session token invalid or expired"})
            else:
                session: UserSession = SESSION_TOKEN_LIST.get(session_token)
                if session.expires < datetime.now():
                    return JSONResponse(status_code=403, content={"detail": "Session expired"})
                elif request.method in ADMIN_METHODS:
                    if not crud.get_user(db=next(get_db()), username=session.username).is_admin:
                        return JSONResponse(status_code=403, content={"detail": "Permission denied"})
        response = await call_next(request)
        return response
