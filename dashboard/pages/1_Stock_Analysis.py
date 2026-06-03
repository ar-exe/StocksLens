import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config import settings

import streamlit as st
import plotly.graph_objects as go
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
st.set_page_config(page_title='Stock Analysis',layout='wide')

with st.sidebar:
    st.header('Controls')
    summary = load_summary()
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

row = summary[summary['ticker'] == ticker]

if row.empty:
    st.warning(f'No available data for {ticker}.')
    st.stop()

row = row.iloc[0]

icon = {"BULLISH": "🟢", "BEARISH": "🔴", "NEUTRAL": "🟡"}.get(
    row["trend_signal"], "⚪"
)

st.title(f"{icon} {ticker}")
st.caption(f"Last updated: {row['price_date']}")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    'Last Close',
    f"${row['last_close']:.2f}",
    delta=f"{row['pct_change_1d']:+.1f}%"
)
c2.metric(
    'Sentiment Score',
    f"{row['sentiment_score']:+.2f}"
)
c3.metric(
    'Health Score',
    f"{row['health_score']:+.1f} / 10"
)
c4.metric(
    'News this week',
    int(row['news_count_7d'])
)
st.divider()

#Price Chart
st.subheader("Price History")
if prices.empty:
    st.info(f"No price data available for {ticker}.")
else:
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=prices['date'],
            open=prices['open'],
            high=prices['high'],
            low=prices['low'],
            close=prices['close'],
            name='Price',
            increasing_line_color="#16a34a",
            decreasing_line_color="#dc2626"
        )
    )
    fig.add_trace(
        go.Bar(
            x=prices['date'],
            y=prices['volume'],
            name='Volume',
            marker_color="rgba(99,102,241,0.25)",
            yaxis="y2"
        )
    )
    fig.update_layout(
        height=380,
        xaxis_rangeslider_visible=False,
        yaxis=dict(title="Price ($)", side="left"),
        yaxis2=dict(
            title="Volume",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        legend=dict(orientation="h", y=1.05),
        margin=dict(l=0, r=0, t=10, b=0),
        hovermode="x unified"     # all traces show on hover together
    )
    st.plotly_chart(fig, use_container_width=True)
st.divider()

col_left, col_right = st.columns([1, 1])
with col_left:
    st.subheader('Sentiment Trend')
    if news.empty:
        st.info(f'No news sentiment data for {ticker}.')
    else:
        news["date"] = pd.to_datetime(news['published_at']).dt.date
        news['signed_score'] = news.apply(
            lambda r: r['score'] if r['label'] == 'positive'
                else -r['score'] if r['label'] == 'negative'
                else 0,
            axis = 1
        )
        daily_sent = (
            news.groupby('date')['signed_score'].mean().reset_index().rename(columns={'signed_score': 'sentiment'})
        )
        fig2 = px.bar(
            daily_sent,
            x='date',
            y='sentiment',
            color='sentiment',
            color_continuous_scale=["#dc2626", "#f59e0b", "#16a34a"],
            range_color=[-1, 1],
            labels={"sentiment": "Avg sentiment", "date": ""}
        )
        fig2.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        fig2.update_layout(
            height=280,
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig2, use_container_width=True)
with col_right:
    st.subheader('Recent News')
    LABEL_ICON = {"positive": "🟢", "negative": "🔴", "neutral": "🟡"}
    if news.empty:
        st.info(f'No Available recent news for {ticker}.')
    else:
        for _, article in news.head(7).iterrows():
            icon = LABEL_ICON.get(article['label'],"⚪" )
            # conf = article['confidence']
            label = article['label']
            st.markdown(f"{icon} [{article['headline']}]({article['url']})")
            st.caption(
                f"{article['source']}  ·  "
                f"{str(article['published_at'])[:10]}  ·  "
                f"**{label}**)"
            )

st.divider()

st.subheader('Sentiment Breakdown')
if news.empty:
    st.info('No availabel sentiment breakdown for now sorry!')
else:
    pos = int(row['positive_count'])
    neg = int(row['negative_count'])
    neu = int(row['neutral_count'])
    total = neg + pos + neu

    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Positive", pos, f"{pos/total:.0%}" if total else None)
    b1.metric("Negative", neg, f"{neg/total:.0%}" if total else None)
    b1.metric("Neutral", neu, f"{neu/total:.0%}" if total else None)
    b1.metric("Total", total)
st.divider()

st.subheader("Fundamentals")

if funds:
    f1, f2, f3, f4 = st.columns(4)
    def fmt(val, suffix=""):
        return f"{val:.2f}{suffix}" if val is not None else "--"
    f1.metric('P/E Ratio', fmt(funds.get('pe_ratio')))
    f2.metric('EPS growth (YoY)', fmt(funds.get('eps_growth'), "%"))
    f3.metric('Beta', fmt(funds.get('beta')))
    high = funds.get('high_52w')
    low = funds.get('low_52w')
    f4.metric(
        "52W range",
        f"${low:.0f} : ${high:.0f}" if high and low else '__'
    )
    #Where current price set in the 52-week range?
    if high and low and high != low:
        position = (row['last_close'] - low) / (high - low)
        st.caption(f"Current price is at **{position:.2f}** point of its 52-week range")
        st.progress(float(position))
else:
    st.info(f"No fundamentals available for {ticker}.")


if row['insider_tx_count'] > 0:
    st.divider()
    st.subheader('Insider Activity (30 days)')
    bought = int(row['insider_bought'])
    sold = int(row['insider_sold'])
    net = bought - sold

    i1, i2, i3 = st.columns(3)
    i1.metric("Shares bought", f'{bought:,}')
    i1.metric("Shares Sold", f'{sold:,}')
    i1.metric("Net", f'{net:,}', delta_color='normal' if net >=0 else 'inverse')