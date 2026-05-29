from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    finnhub_key: str
    watchlist: List[str] = ["AAPL", "NVDA", "TSLA", "MSFT", "AMZN"]
    prices_collection_period: str = "1y"
    news_from: str = "2026-01-01"
    news_to: str = "2026-03-10"
    insider_trans_from: str = "2026-01-01"
    insider_trans_to: str = "2026-03-10"
    analyze_news_published_at: str = "2026-01-01"

    class Config:
        env_file = ".env"

settings = Settings()