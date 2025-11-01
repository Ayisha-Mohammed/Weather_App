from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    OPENWEATHER_API_KEY: str
    JWT_SECRET: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), ".env")

settings = Settings()
