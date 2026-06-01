import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import json
# from data_pipeline.collectors.news import collect_news
# from data_pipeline.collectors.prices import collect_prices
from config import settings
from loader import (
    load_fundamentals,
    load_insider_trans,
    load_news,
    load_summary,
    load_prices
)
from singals import derive_health_score, derive_trend_signal

st.set_page_config(page_title='Stock Analysis',layout='wide')

with st.sidebar:
    st.header('Controls')
    ticker = st.selectbox(
        "Stock",
        settings.watchlist
    )
    days = st.select_slider(
        "Price History",
        options=[30, 60, 90, 180, 365],
        value=90
    )
    st.divider()
    if st.button("Refresh"):
        st.cache_data.clear()
        st.rerun()

prices = load_prices(ticker, days)
news = load_news(ticker, published_at=settings.analyze_news_published_at, limit=7)
funds = load_fundamentals(ticker)



