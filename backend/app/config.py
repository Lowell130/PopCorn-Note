#app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DB: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    TMDB_API_KEY: str = ""  # 👈 aggiunto

    class Config:
        env_file = ".env"

settings = Settings()

