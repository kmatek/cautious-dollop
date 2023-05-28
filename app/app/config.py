import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABSE_URL: str = os.environ.get('DATABASE_URL')
    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    ALGORITHM: str = os.environ.get('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 30)
    TOKEN_TYPE: str = 'Bearer'


settings = Settings()
