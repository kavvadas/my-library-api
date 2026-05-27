from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    API_KEY: str
    APP_VERSION: str
    JWT_KEY: str

    model_config = ConfigDict(env_file=".env")

settings = Settings()