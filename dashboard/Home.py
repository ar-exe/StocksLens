import streamlit as st
import pandas as pd
import plotly.express as px
from data_pipeline.database.connection import get_connection

st.set_page_config(
    page_title="StockLens", 
    page_icon="📈",
    layout="wide"
)

st.title("StockLens")
st.caption("Daily AI-powered analysis across your watchlist")

@st.cache_data(ttl=3600)
def load_watchlist_summary():
    conn = get_connection()
    df = pd.read_sql("""
        SELECT 
            a.ticker,
            a.trend_signal,
            a.sentiment_score,
            a.health_score,
            a.analysis_date,
            p.close as last_price,
            p.close - LAG(p.close) OVER (PARTITION BY p.ticker ORDER BY p.date) as price_change
        FROM analysis_results a
        JOIN prices p ON a.ticker = p.ticker
        WHERE a.analysis_date = (SELECT MAX(analysis_date) FROM analysis_results)
          AND p.date = (SELECT MAX(date) FROM prices)
        ORDER BY a.health_score DESC
    """, conn)
    conn.close()
    return df

df = load_watchlist_summary()

# Colour-coded signal cards
cols = st.columns(len(df))
for col, (_, row) in zip(cols, df.iterrows()):
    color = {"BULLISH": "🟢", "BEARISH": "🔴", "NEUTRAL": "🟡"}.get(row.trend_signal, "⚪")
    col.metric(
        label=f"{color} {row.ticker}",
        value=f"${row.last_price:.2f}",
        delta=f"{row.price_change:+.2f}"
    )
    col.caption(f"Health: {row.health_score:.1f}/10")