import pandas as pd
import numpy as np
import yfinance as yf
import psycopg2
from datetime import date, timedelta, datetime
import json
import finnhub
from psycopg2.extras import RealDictCursor



def collect_raw_fundemantals(ticker: str,finnhub_client, conn):
    data = finnhub_client.company_basic_financials(ticker, 'all')
    metrics = data['metric']
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO raw_stock_fundamentals
                    (ticker, payload)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING""", (ticker, json.dumps(metrics)))
    conn.commit()