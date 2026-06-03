import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config import settings

import streamlit as st
# import plotly.graph_objects as go
import plotly.express as px
import json
# from data_pipeline.collectors.news import collect_news
# from data_pipeline.collectors.prices import collect_prices
from config import settings
from dashboard.loader import (
    load_fundamentals,
    load_insider_trans,
    load_news,
    load_summary,
    load_prices
)
from dashboard.signals import derive_health_score, derive_trend_signal
import pandas as pd

st.set_page_config(page_title='Sector Overview –– StocksLens', layout='wide')

st.title('Sector Overview')
st.caption('All tracked stocks compared side by side')

df = load_summary()
if df.empty:
    st.warning('No data yet')
    st.stop()

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader('Signal Breakdown')
    counts = df['trend_signal'].value_counts().reset_index()
    counts.columns = ['Signal', 'Count']
    fig_pie = px.pie(
        counts,
        names='Signal',
        values='Count',
        color="Signal",
        color_discrete_map={
            "BULLISH": "#16a34a",
            "BEARISH": "#dc2626",
            "NEUTRAL": "#d97706"
        },
        hole=0.45
    )
    fig_pie.update_layout(
        height=260,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(orientation='h', y=-0.1)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader('Health vs Sentiment')
    st.caption('Each bubble is a stock, positions shows both dimensions at once')
    fig_scatter = px.scatter(
        df,
        x='sentiment_score',
        y='health_score',
        text='ticker',
        color="trend_signal",
        color_discrete_map={
            "BULLISH": "#16a34a",
            "BEARISH": "#dc2626",
            "NEUTRAL": "#d97706"
        },
        hover_data=["last_close", "pct_change_7d"]
    )
    fig_scatter.update_traces(
        textposition="top center",
        marker=dict(size=16, opacity=0.85)
    )
    fig_scatter.add_vline(
        x=0, line_dash="dash",
        line_color="gray", opacity=0.4
    )
    fig_scatter.add_hline(
        y=5, line_dash="dash",
        line_color="gray", opacity=0.4
    )
    fig_scatter.update_layout(
        height=260,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis_title="Sentiment score (FinBERT)",
        yaxis_title="Health score"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

st.subheader('30-day performance (normalized to 100)')
st.caption('all prices have been rebased to 100 at the start, to show relative performance')
all_prices = []
for t in df['ticker']:
    p = load_prices(t, 30)
    if not p.empty:
        p = p.sort_values('date').copy()
        start_price = p['close'].iloc[0]
        if start_price > 0:
            p['normalized'] = (p['close'] / start_price) * 100
            p['ticker'] = t
            all_prices.append(p[['date', 'normalized', 'ticker']])

if all_prices:
    combined = pd.concat(all_prices)
    fig_lines = px.line(
        combined,
        x="date",
        y="normalized",
        color="ticker",
        labels={"normalised": "Rebased (100 = start)", "date": ""}
    )
    fig_lines.add_hline(
        y=100, line_dash="dot",
        line_color="gray", opacity=0.5
    )
    fig_lines.update_layout(
        height=320,
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode="x unified"
    )
    st.plotly_chart(fig_lines, use_container_width=True)