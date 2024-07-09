""" ./config.py"""

import os
from pydantic import BaseSettings


class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://tts_user:tts_eugene@localhost/tts_app"
    # Add other configuration settings here


settings = Settings()
