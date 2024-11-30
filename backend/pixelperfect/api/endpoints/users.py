from fastapi import APIRouter, Cookie, Depends
from sqlmodel import Session
from typing import Annotated

from pixelperfect.db import crud
from pixelperfect.db.database import get_db
from pixelperfect.db.models import UserBase

router = APIRouter()


@router.get("/me", response_model=UserBase, status_code=200)
def get_current_user(session_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    if session_token:
        user_session = crud.get_user_session(db=db, session_token=session_token)
        if user_session:
            user = crud.get_user(db=db, username=user_session.username)
            return user
