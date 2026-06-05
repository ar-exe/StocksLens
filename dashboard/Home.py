import streamlit as st
from loader import load_summary


st.set_page_config(
    page_title="StocksLens",
    layout="wide"
)

st.title("StocksLens")
st.caption("Daily Stocks Intelligence Dashboard -- updated every weekday at 07:00 UTC")
st.divider()

df = load_summary()
if df.empty:
    st.warning('No analysis data yet, run the pipeline first')
    st.stop()

st.subheader("Watchlist")
cols = st.columns(len(df))

SIGNAL_ICON = {"BULLISH": "🟢", "BEARISH": "🔴", "NEUTRAL": "🟡"}

for col, (_, row) in zip(cols, df.iterrows()):
    icon  = SIGNAL_ICON.get(row.trend_signal, "⚪")
    delta = f"{row.price_change_1d:.2f}" if row.price_change_1d else None
    col.metric(
        label=f"{icon} {row.ticker}",
        value=f"${row.last_close:.2f}",
        delta=delta
    )
    col.caption(f"Health: {row.health_score:.1f}/10")
    col.caption(f"Sentiment: {row.sentiment_score:+.2f}")

st.divider()
# Home.py — after your watchlist summary section
st.divider()
st.subheader("Explore")

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link(
        "pages/1_Stock_Analysis.py",
        label="Stock Analysis",
        icon="📊"
    )
    st.caption("Deep dive into any stock — price chart, sentiment history, news, insider activity")

with col2:
    st.page_link(
        "pages/2_Sector_Overview.py",
        label="Sector Overview",
        icon="🗺️"
    )
    st.caption("Compare all tracked stocks — signals, momentum, health scores side by side")

# with col3:
#     st.page_link(
#         "pages/3_Peers.py",
#         label="Peer Analysis",
#         icon="🔗"
#     )
#     st.caption("Sector peers and correlated stocks for any ticker")


st.subheader("Overview")

# Style the trend signal column
def style_signal(val):
    colors = {"BULLISH": "#166534", "BEARISH": "#991b1b", "NEUTRAL": "#92400e"}
    return f"color: {colors.get(val, 'inherit')}; font-weight: 500"

styled = df[["ticker","trend_signal","sentiment_score","health_score","last_close"]]\
    .rename(columns={
        "ticker":          "Ticker",
        "trend_signal":    "Signal",
        "sentiment_score": "Sentiment",
        "health_score":    "Health",
        "last_close":      "Last Price",
        # "analysis_date":   "Updated"
    })\
    .style.applymap(style_signal, subset=["Signal"])\
    .format({
        "Sentiment":  "{:+.2f}",
        "Health":     "{:.1f}",
        "Last Price": "${:.2f}"
    })

st.dataframe(styled, use_container_width=True, hide_index=True)

# ── Last updated footer ──────────────────────────────────
# st.caption(f"Last pipeline run: {df.analysis_date.max()}")