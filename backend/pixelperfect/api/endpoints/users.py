from fastapi import APIRouter, Cookie, Depends
from sqlmodel import Session
from typing import Annotated

from pixelperfect.db import crud
from pixelperfect.db.database import get_db
from pixelperfect.db.models import UserBase
from pixelperfect.security.middleware import SESSION_TOKEN_LIST

router = APIRouter()


@router.get("/me", response_model=UserBase, status_code=200)
def get_current_user(session_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    if session_token:
        session = SESSION_TOKEN_LIST.get(session_token)
        user = crud.get_user(db=db, username=session.username)
        return user
