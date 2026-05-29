
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str      
    finnhub_key: str
    # alphavantage_key: str
    # anthropic_key: str

    class Config:
        env_file = ".env"

settings = Settings()