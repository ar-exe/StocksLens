import pandas as pd
import numpy as np
import yfinance as yf
import psycopg2
from datetime import date, timedelta, datetime
import json
import finnhub


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



def collect_news(ticker: str, d_from: str, d_to:str, conn):
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


def collect_peers(ticker: str, conn):
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

def collect_insider_transactions(ticker: str, d_from: str, d_to: str, conn):
    data = finnhub_client.stock_insider_transactions(ticker, d_from, d_to)
    data = pd.DataFrame(data['data'])
    data.reset_index(inplace=True)
    with conn.cursor() as cur:
        for _, row in data.iterrows():
            cur.execute("""
                INSERT INTO insider_trans
                (ticker, change, name, filingdate, transdate, share, transcode, transprice)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING """,(
                    ticker,
                    row['change'],
                    row['name'],
                    row['filingDate'],
                    row['transactionDate'],
                    row['share'],
                    row['transactionCode'],
                    row['transactionPrice']
                ))
    conn.commit()

import json
def collect_raw_fundemeentals(ticker: str, conn):
    data = finnhub_client.company_basic_financials(ticker, 'all')
    metrics = data['metric']
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO raw_stock_fundamentals
                    (ticker, payload)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING""", (ticker, json.dumps(metrics)))
    conn.commit()