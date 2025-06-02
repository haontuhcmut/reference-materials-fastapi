from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi.templating import Jinja2Templates

from app.auth.schema import CreateUserModel
from app.config import Config
from app.db.model import User
from app.error import EmailAlreadyExist, UsernameAlreadyExist, UseNotFound
from app.utility.security import encode_url_safe_token, get_hashed_password, decode_url_safe_token
from app.celery_task import send_email

templates = Jinja2Templates(directory="app/html_template") #or can use Path from pathlib base_dir

class UserService:

    async def existing_checker(self, field_check: str, value: str, session: AsyncSession):
        statement = select(User).where(getattr(User, field_check) == value)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def create_user(self, user_data: CreateUserModel, session: AsyncSession):
        user_data_dict = user_data.model_dump(exclude={"password"})
        new_user = User(**user_data_dict)
        new_user.hashed_password = get_hashed_password(user_data.password)
        new_user.role = "user"
        session.add(new_user)
        await session.commit()
        return new_user

    async def update_user(self, user_data: dict, session: AsyncSession):
        for key, value in user_data.items():
            setattr(User, key, value)
        await session.commit()
        return User

    async def signup_user(self, user_data: CreateUserModel, session: AsyncSession):
        existing_email = await self.existing_checker("email", user_data.email, session)
        if existing_email is not None:
            raise EmailAlreadyExist()

        existing_username = await self.existing_checker("username", user_data.username, session)
        if existing_username:
            raise UsernameAlreadyExist()

        new_user = await self.create_user(user_data, session)

        #Encoding url token
        token = encode_url_safe_token(
            {"email": user_data.email}
        )  # Using URLSafeTimedSerializer encode
        link = f"http://{Config.DOMAIN}/{Config.VERSION}/oauth/verify/{token}"
        html_content = templates.get_template("verify_email.html").render(
            {"action_url": link, "first_name": user_data.first_name}
        )

        #Email sending
        emails = [user_data.email]
        subject = "Verification your email"
        send_email.delay(emails, subject, html_content)
        return new_user

    async def verify_user_account(self, token: str, session: AsyncSession):
        token_data = decode_url_safe_token(token)
        user_email = token_data.get("email")
        if user_email:
            user = await self.existing_checker("email", user_email, session)
            if not user:
                raise UseNotFound()
            await self.update_user()