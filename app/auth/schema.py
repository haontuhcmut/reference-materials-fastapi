from pydantic import BaseModel, Field


class CreateUserModel(BaseModel):
    email: str
    username: str = Field(max_length=32)
    last_name: str = Field(max_length=32)
    first_name: str = Field(max_length=32)
    password: str = Field(max_length=32)

class UserLoginModel(BaseModel):
    email: str = Field(max_length=32)
    password: str = Field(max_length=32)

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


