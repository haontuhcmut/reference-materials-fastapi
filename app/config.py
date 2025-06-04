from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / ".env"

class Settings(BaseSettings):
    DATABASE_URL: str
    DOMAIN: str
    VERSION: str
    SECRET_KEY: str
    SALT: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JTI_EXPIRY_SECOND: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_SERVER: str

    BROKER_URL: str
    BACKEND_URL: str


    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")


Config = Settings()


#Celery config
broker_url = Config.BROKER_URL
backend_url = Config.BACKEND_URL
broker_connection_retry_on_startup = True

