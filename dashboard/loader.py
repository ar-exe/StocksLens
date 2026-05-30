import streamlit as st
import pandas as pd
import psycopg2
from config import settings
from data_pipeline.database.connection import get_connection, put_connection

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
    return df

@st.cache_data(ttl=3600)
def load_news(ticker: str, published_at: str, limit: int) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql("""
                    SELECT headline, source, url, raw_content, label, score
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