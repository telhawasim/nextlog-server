from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017/"
    DB_NAME: str = "nextlog"

    class Config:
        env_file = ".nextlog-env"


settings = Settings()
