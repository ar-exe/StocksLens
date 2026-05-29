import pandas as pd
import numpy as np
import yfinance as yf
import psycopg2
from datetime import date, timedelta, datetime
import json
import finnhub
from psycopg2.extras import RealDictCursor
from transformers import pipeline

def ensure_stock_exists(ticker, conn):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO stocks (ticker)
            VALUES (%s)
            ON CONFLICT DO NOTHING
        """, (ticker,))
    conn.commit()

def collect_prices(ticker: str, period: str, conn):
    ensure_stock_exists(ticker=ticker, conn=conn)
    tik = yf.Ticker(ticker)
    df = tik.history(period=period)

    df.reset_index(inplace=True)

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