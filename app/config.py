import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABSE_URL: str = os.environ.get('DATABASE_URL')


settings = Settings()
