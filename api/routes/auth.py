from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.exceptions import INVALID_CREDENTIALS_EXCEPTION
from api.models import UserRegistration
from core.auth import create_access_token, hash_password, password_correct
from database.database import create_user, get_db_conn, get_user_by_username

auth_router = APIRouter(prefix="/auth", tags=["authenticate"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_registration: UserRegistration,
    db_conn: Annotated[Connection, Depends(get_db_conn)],
):
    hashed_password = hash_password(user_registration.raw_password)
    result = await create_user(db_conn, user_registration.username, hashed_password)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    return {"message": "User registered successfully"}


@auth_router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_conn: Annotated[Connection, Depends(get_db_conn)],
):
    db_user = await get_user_by_username(db_conn, form_data.username)

    if not db_user or not password_correct(form_data.password, db_user.hashed_password):
        raise INVALID_CREDENTIALS_EXCEPTION

    access_token = create_access_token(data={"sub": db_user.username})

    return {"access_token": access_token, "token_type": "bearer"}
