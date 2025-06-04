from fastapi import APIRouter, status, Depends
from typing import Annotated

from app.auth.schema import CreateUserModel, TokenModel, UserLoginModel, UserModel
from app.db.dependency import SessionDep
from app.auth.service import UserService
from app.auth.denpendency import get_current_user, RefreshTokenBearer


user_service = UserService()
oauth_route = APIRouter()


@oauth_route.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: CreateUserModel, session: SessionDep):
    new_user = await user_service.signup_user(user_data, session)
    return {
        "message": "Account created! Check email to verify your email",
        "user": new_user,
    }


@oauth_route.get("/verify/{token}")
async def verify_user_account(token: str, session: SessionDep):
    token_safe_url = await user_service.verify_user_account(token, session)
    return token_safe_url


@oauth_route.post("/login", response_model=TokenModel)
async def user_login(login_data: UserLoginModel, session: SessionDep):
    token_response = await user_service.login_user(login_data, session)
    return token_response

@oauth_route.get("/me", response_model=UserModel)
async def get_current_user(user: Annotated[UserModel, Depends(get_current_user)]):
    return user


