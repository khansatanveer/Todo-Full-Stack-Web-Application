from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings
    """
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configure the source of environment variables
    model_config = SettingsConfigDict(
        env_file=".env",  # Load from .env file
        extra="ignore"  # Ignore extra environment variables not defined here
    )

settings = Settings()