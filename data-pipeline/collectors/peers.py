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
        name='Collect Peers',
        cache_key_fn=task_input_hash,
        cache_expiration=timedelta(hours=23),
        retries=3,
        retry_delay_seconds=10
)
def collect_peers(ticker: str,finnhub_client, conn):
    peers = finnhub_client.company_peers(ticker)
    with conn.cursor() as cur:
        for i in peers:
            cur.execute("""
                        INSERT INTO stocks (ticker)
                        VALUES (%s)
                        ON CONFLICT DO NOTHING """, (i,))
            cur.execute("""
                        INSERT INTO stock_peers 
                        (ticker, peer_ticker)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                        """,(
                            ticker, 
                            i
                        ))
    conn.commit()