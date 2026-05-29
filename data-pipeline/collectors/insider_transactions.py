import pandas as pd
import numpy as np
import yfinance as yf
import psycopg2
from datetime import date, timedelta, datetime
import json
import finnhub
from psycopg2.extras import RealDictCursor
from transformers import pipeline

def collect_insider_transactions(ticker: str, d_from: str, d_to: str,finnhub_client, conn):
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