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
from data_pipeline.database.connection import get_connection, put_connection

@task(
        name='Collect Insider Transactions',
        cache_key_fn=task_input_hash,
        cache_expiration=timedelta(hours=23),
        retries=3,
        retry_delay_seconds=10
)
def collect_insider_transactions(ticker: str, d_from: str, d_to: str,finnhub_client):
    conn = get_connection()
    data = finnhub_client.stock_insider_transactions(ticker, d_from, d_to)
    data = pd.DataFrame(data['data'])
    data.reset_index(inplace=True)
    with conn.cursor() as cur:
        for _, row in data.iterrows():
            cur.execute("""
                INSERT INTO insider_transactions
                (ticker, change_amount, name, filing_date, transaction_date, shares, transaction_code, transaction_price)
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
    put_connection(conn)