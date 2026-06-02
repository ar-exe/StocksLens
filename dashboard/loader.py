
import sys
import os

# Corrected: Add the project root to sys.path
# This should go up one level from 'dashboard' to 'StocksLens'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
import streamlit as st
import pandas as pd
import psycopg2
# from config import settings
from data_pipeline.database.connection import get_connection, put_connection
from dashboard.signals import derive_health_score, derive_trend_signal

@st.cache_data(ttl=3600)
def load_prices(ticker: str, days: int) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql("""
                    SELECT date, open, high, low, close, volume
                    FROM prices 
                    WHERE ticker = %s
                    ORDER BY date DESC
                    LIMIT %s
                    """, conn, params=(ticker, days))
    put_connection(conn)
    return df

@st.cache_data(ttl=3600)
def load_peers(ticker: str) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql("""
                    SELECT peer_ticker
                    FROM stock_peers
                    WHERE ticker = %s
                    """, conn, params=(ticker,))
    put_connection(conn)
    return df

@st.cache_data(ttl=3600)
def load_fundamentals(ticker: str) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql("""
                    SELECT payload
                    FROM raw_stock_fundamentals
                    WHERE ticker = %s
                    ORDER BY curated_at DESC
                    """, conn, params=(ticker,))
    put_connection(conn)
    if df.empty:
        return {}
    payload = df.iloc[0]['payload']
    return{
        "pe_ratio":       payload.get("peNormalizedAnnual"),
        "eps_growth":     payload.get("epsGrowthTTMYoy"),
        "revenue_growth": payload.get("revenueGrowthTTMYoy"),
        "debt_equity":    payload.get("totalDebt/totalEquityAnnual"),
        "roe":            payload.get("roeTTM"),
        "high_52w":       payload.get("52WeekHigh"),
        "low_52w":        payload.get("52WeekLow"),
        "beta":           payload.get("beta"),

    }

@st.cache_data(ttl=3600)
def load_news(ticker: str, published_at: str, limit: int) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql("""
                    SELECT headline, source, url, raw_content, label, score, published_at
                    FROM news_articles
                    WHERE ticker = %s
                    AND published_at >= %s
                    ORDER BY published_at DESC
                    LIMIT %s
                    """, conn, params=(ticker, published_at, limit))
    put_connection(conn)
    return df

@st.cache_data(ttl=3600)
def load_insider_trans(ticker: str) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql("""
                    SELECT change, name, fillingdate, transdate, share, transcode, transprice
                    FROM insider_trans
                    WHERE ticker = %s
                    ORDER BY fillingdate
                    """, conn, params=(ticker,))
    put_connection(conn)
    return df

@st.cache_data(ttl=3600)
def load_summary()-> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql("""
                    WITH
                    latest_prices AS (
                        SELECT DISTINCT ON (ticker)
                            ticker,
                            date    AS price_date,
                            close   AS last_close,
                            open    AS last_open,
                            volume  AS last_volume
                        FROM prices
                        ORDER BY ticker, date DESC
                     ),
                    prev_prices AS (
                        SELECT DISTINCT ON (ticker)
                            ticker,
                            close AS prev_close
                        FROM prices
                     WHERE date < (SELECT MAX(date) FROM prices)
                     ORDER BY ticker, date DESC
                     ),
                    week_ago_prices AS (
                        SELECT DISTINCT ON (ticker)
                            ticker,
                            close AS week_ago_close
                        FROM prices
                        WHERE date <= CURRENT_DATE - INTERVAL '7 days'
                        ORDER BY ticker, date DESC
                     ),
                    price_stats AS (
                        SELECT 
                            ticker,
                            STDDEV(close)  AS volatility_30d,
                            MAX(close)     AS high_30d,
                            MIN(close)     AS low_30d,
                            AVG(volume)    AS avg_volume_30d
                        FROM prices
                        WHERE date >= CURRENT_DATE - INTERVAL '30 days'
                        GROUP BY ticker
                     ),
                    news_sentiment AS(
                        SELECT
                            ticker,
                            COUNT(*) AS news_count_7d,
                            AVG(
                                CASE
                                    WHEN label = 'positive' THEN score
                                    WHEN label = 'negative' THEN -score
                                    ELSE 0
                                END
                              )       AS sentiment_score,
                            SUM(CASE WHEN label = 'positive' THEN 1 ELSE 0 END) AS positive_count,
                            SUM(CASE WHEN label = 'negative' THEN 1 ELSE 0 END) AS negative_count,
                            SUM(CASE WHEN label = 'neutral' THEN 1 ELSE 0 END) AS neutral_count
                        FROM news_articles
                        WHERE published_at >= CURRENT_DATE - INTERVAL '7 days'
                        AND label IS NOT NULL
                        GROUP BY ticker
                     ),
                    insider_transactions AS (
                        SELECT
                            ticker,
                            SUM(CASE WHEN transaction_code = 'P' THEN change_amount ELSE 0 END) AS shares_bought,
                            SUM(CASE WHEN transaction_code = 'S' THEN ABS(change_amount) ELSE 0 END) AS shares_sold,
                            COUNT(*) AS insider_transactions
                        FROM insider_transactions
                        WHERE transaction_date >= CURRENT_DATE - INTERVAL '30 days'
                        GROUP BY ticker
                     )
                    SELECT
                        lp.ticker,
                        lp.price_date,
                        lp.last_close,
                        lp.last_volume,
                        ROUND((lp.last_close - pp.prev_close)::numeric, 2)
                            AS price_change_1d,
                        ROUND(((lp.last_close - pp.prev_close) / pp.prev_close * 100)::numeric, 2)
                            AS pct_change_1d,
                        ROUND(((lp.last_close - wa.week_ago_close) / wa.week_ago_close * 100)::numeric, 2)
                            AS pct_change_7d,
                     
                        ROUND(ps.volatility_30d::numeric, 2) AS volatility_30d,
                        ROUND(ps.high_30d::numeric, 2) AS high_30d,
                        ROUND(ps.low_30d::numeric, 2) AS low_30d,
                        ROUND(lp.last_volume / NULLIF(ps.avg_volume_30d, 0)::numeric, 2) AS volume_ratio,

                        COALESCE(ROUND(ns.sentiment_score::numeric, 3), 0) AS sentiment_score,
                        COALESCE(ns.news_count_7d, 0) AS news_count_7d,
                        COALESCE(ns.positive_count, 0) AS positive_count,
                        COALESCE(ns.negative_count, 0) AS negative_count,
                        COALESCE(ns.neutral_count, 0) AS neutral_count,
                     
                        COALESCE(ia.shares_bought, 0) AS insider_bought,
                        COALESCE(ia.shares_sold, 0) AS insider_sold,
                        COALESCE(ia.insider_transactions, 0) AS insider_tx_count
                     FROM latest_prices lp
                     LEFT JOIN prev_prices pp ON lp.ticker = pp.ticker
                     LEFT JOIN week_ago_prices wa ON lp.ticker = wa.ticker
                     LEFT JOIN price_stats ps ON lp.ticker = ps.ticker
                     LEFT JOIN news_sentiment ns ON lp.ticker = ns.ticker
                     LEFT JOIN insider_transactions ia ON lp.ticker = ia.ticker

                     ORDER BY sentiment_score DESC
                    """, conn)
    put_connection(conn)
    df['trend_signal'] = df.apply(derive_trend_signal, axis=1)
    df['health_score'] = df.apply(derive_health_score, axis=1)
    return df