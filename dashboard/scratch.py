# scratch.py
import streamlit as st
import pandas as pd
import numpy as np

# ── Text elements ───────────────────────────────
st.title("StockLens")
st.subheader("Daily intelligence")
st.caption("Data updated at 07:00 UTC")
st.divider()

# ── Metric cards ────────────────────────────────
# metric(label, value, delta)
# delta turns green if positive, red if negative
col1, col2, col3, col4 = st.columns(4)
col1.metric("AAPL",  "$182.50", "+1.2%")
col2.metric("NVDA",  "$431.20", "-0.8%")
col3.metric("TSLA",  "$248.90", "+3.1%")
col4.metric("MSFT",  "$378.40", "+0.4%")

st.divider()

# ── Sidebar ─────────────────────────────────────
with st.sidebar:
    st.header("Controls")
    ticker = st.selectbox("Stock", ["AAPL", "NVDA", "TSLA", "MSFT"])
    days   = st.slider("History (days)", 30, 365, 90)
    st.caption(f"Showing {days} days for {ticker}")

# ── Tabs ────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["Price", "Sentiment", "News"])

with tab1:
    # Fake data for now — replace with real DB queries later
    df = pd.DataFrame({
        "date":  pd.date_range(end="2024-01-01", periods=days),
        "close": np.random.randn(days).cumsum() + 180
    })
    st.line_chart(df.set_index("date")["close"])

with tab2:
    st.write("Sentiment chart goes here")

with tab3:
    st.write("News feed goes here") 