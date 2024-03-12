from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from typing import Annotated

from src.auth.models import Users
from src.auth.schemas import CreateUserRequest, Token
from src.auth.services import create_db_user, authenticate_user
from src.auth.utils import bcrypt_context, create_access_token
from src.database import db_dependency

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, request: CreateUserRequest):
    create_user_model = Users(
        email=request.email,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        hashed_password=bcrypt_context.hash(request.password),
        is_active=True
    )

    create_db_user(db, create_user_model)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {
        'access_token': token,
        'token_type': 'bearer',
    }
