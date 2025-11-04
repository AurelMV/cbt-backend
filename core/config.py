from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Security settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Database URL
    DATABASE_URL: str

    # CORS settings
    CORS_ORIGINS: list[str] = []
    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    class Config:
        env_file = ".env"
