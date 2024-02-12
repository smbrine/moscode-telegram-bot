import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    TG_BOT_TOKEN: str
    PUBLIC_ADDR: str
    ADMIN_CHAT_ID: int
    KAFKA_URL: str
    DEBUG: bool = False
    LISTEN_ADDR: str
    LISTEN_PORT: int
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
