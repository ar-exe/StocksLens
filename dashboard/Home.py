import streamlit as st

st.set_page_config(
    page_title="StocksLens",
    layout="wide"
)

st.title("StocksLens")
st.caption("Daily Stocks Intelligence Dashboard -- updated every weekday at 07:00 UTC")
st.divider()

st.subheader("Watchlist")
cols = st.columns(len(df))