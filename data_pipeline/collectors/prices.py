import pandas as pd
import numpy as np
import yfinance as yf
import psycopg2
from datetime import date, timedelta, datetime
import json
import finnhub
from psycopg2.extras import RealDictCursor
from transformers import pipeline
from data_pipeline.database.connection import get_connection, put_connection
def ensure_stock_exists(ticker, conn):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO stocks (ticker)
            VALUES (%s)
            ON CONFLICT DO NOTHING
        """, (ticker,))
    # conn.commit()
    # put_connection(conn)
from prefect import task
from prefect.tasks import task_input_hash


@task(
        name='Collect Stock Prices',
        cache_key_fn=task_input_hash,
        cache_expiration=timedelta(hours=23),
        retries=3,
        retry_delay_seconds=10
)
def collect_prices(ticker: str, period: str):

    tik = yf.Ticker(ticker)

    df = tik.history(period=period)

    df.reset_index(inplace=True)

    conn = get_connection()

    try:

        ensure_stock_exists(ticker=ticker, conn=conn)

        with conn.cursor() as cur:

            for _, row in df.iterrows():

                cur.execute("""

                    INSERT INTO prices

                    (ticker, date, open, high, low, close, volume)

                    VALUES (%s, %s, %s, %s, %s, %s, %s)

                    ON CONFLICT (ticker, date) DO NOTHING

                """, (

                    ticker,

                    row['Date'].date(),

                    float(row['Open']),

                    float(row['High']),

                    float(row['Low']),

                    float(row['Close']),

                    int(row['Volume'])

                ))

        conn.commit()

    except Exception:

        conn.rollback()

        raise

    finally:

        put_connection(conn)