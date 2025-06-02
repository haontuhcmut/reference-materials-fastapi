import logging
from itsdangerous import URLSafeSerializer
from passlib.context import CryptContext

from app.config import Config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

serialize = URLSafeSerializer(
    secret_key=Config.SECRET_KEY,
    salt=Config.SALT,
)

def encode_url_safe_token(data: dict):
    token = serialize.dumps(data)
    return token

def get_hashed_password(password):
    return  pwd_context.hash(password)

def decode_url_safe_token(token: str):
    try:
        token_data = serialize.loads(token)
        return token_data
    except Exception as e:
        logging.error(str(e))




