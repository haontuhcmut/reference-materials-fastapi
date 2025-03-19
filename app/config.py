from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / ".env"

class Settings(BaseSettings):
    DATABASE_URL: str
    VERSION: str

    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")


Config = Settings()

