import pandas as pd
import numpy as np
import yfinance as yf
import psycopg2
from datetime import date, timedelta, datetime
import json
import finnhub
from psycopg2.extras import RealDictCursor


from prefect import task
from prefect.tasks import task_input_hash
from data_pipeline.database.connection import get_connection, put_connection

@task(
        name='Collect Raw Fundamentals',
        cache_key_fn=task_input_hash,
        cache_expiration=timedelta(hours=23),
        retries=3,
        retry_delay_seconds=10
)
def collect_raw_fundemantals(ticker: str,finnhub_client):
    conn = get_connection()
    data = finnhub_client.company_basic_financials(ticker, 'all')
    metrics = data['metric']
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO raw_stock_fundamentals
                    (ticker, payload)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING""", (ticker, json.dumps(metrics)))
    conn.commit()
    put_connection(conn)