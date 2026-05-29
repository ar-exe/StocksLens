import pandas as pd
import numpy as np
import yfinance as yf
import psycopg2
from datetime import date, timedelta, datetime
import json
import finnhub
from psycopg2.extras import RealDictCursor
from transformers import pipeline
from prefect import task
from prefect.tasks import task_input_hash


@task(
        name='Collect News Articles',
        cache_key_fn=task_input_hash,
        cache_expiration=timedelta(hours=23),
        retries=3,
        retry_delay_seconds=10
)
def collect_news(ticker: str, d_from: str, d_to:str,finnhub_client, conn):
    data = pd.DataFrame(finnhub_client.company_news(ticker, _from=d_from, to=d_to))
    data.reset_index(inplace=True)
    data['datetime'] = pd.to_datetime(data['datetime'], unit='s')
    with conn.cursor() as cur:
        for _, row in data.iterrows():
            cur.execute("""
                    INSERT INTO news_articles
                    (ticker, headline, source, url, published_at, raw_content, scraped_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (url) DO NOTHING
""", (
    ticker,
    row['headline'],
    row['source'],
    row['url'],
    row['datetime'],
    row['summary'],
    datetime.now()
))
    conn.commit()