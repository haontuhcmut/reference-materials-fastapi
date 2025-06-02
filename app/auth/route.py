from fastapi import APIRouter, status

from app.auth.schema import CreateUserModel
from app.db.dependency import SessionDep
from app.auth.service import UserService


user_service = UserService()
oauth_route = APIRouter()

@oauth_route.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: CreateUserModel, session: SessionDep):
    new_user = await user_service.signup_user(user_data, session)
    return {
        "message": "Account created! Check email to verify your email",
        "user": new_user
    }

@oauth_route.get("/verify/{token}")
async def verify_user_account(token: str, session: SessionDep):
    token_data =