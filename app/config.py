"""
Module responsible for application configuration settings.
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings class.

    Defines configuration parameters such as database URL,
    secret key, JWT algorithm, and access token expiration minutes.
    """
    DATABASE_URL: str = "postgresql://postgres:nekonime@localhost/FastAPI"
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

# Instantiate settings object
settings = Settings()
