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
        name='Analyze News Articles',
        cache_key_fn=task_input_hash,
        cache_expiration=timedelta(hours=23),
        retries=3,
        retry_delay_seconds=10
)
def analyze_news_articles(ticker: str, published_at: str, classifier=None, conn=None):

    conn = get_connection()
    classifier = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id, headline, source, published_at, raw_content
            FROM news_articles
            WHERE ticker = %s 
            AND published_at >= %s
            ORDER BY published_at DESC
            LIMIT 15;
        """, 
        (ticker, published_at))
        news = cur.fetchall()
        for i in news:
            analysis = classifier(i['raw_content'])
            cur.execute("""
                UPDATE news_articles
                SET label = %s,
                    score = %s
                WHERE id = %s
                        """, (analysis[0]['label'], analysis[0]['score'], i['id']))
    conn.commit()
    put_connection(conn)