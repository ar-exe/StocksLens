# StocksLens
https://stockslens.streamlit.app/


StocksLens is a stock intelligence project that collects market data, news, fundamentals, and insider transactions, stores them in Postgres, analyzes sentiment, and exposes a Streamlit dashboard for exploration.

## Project Overview

StocksLens is built as a data pipeline + dashboard platform for a small watchlist of stocks:
- `AAPL`
- `NVDA`
- `TSLA`
- `MSFT`
- `AMZN`

The project collects:
- historical stock prices
- company news articles
- raw fundamental metrics
- insider transaction filings
- peer relationships
- sentiment analysis on news articles

It also provides a frontend dashboard for stock analysis and sector overview.

## Repository Structure

### Root
- `README.md` – project overview
- `requirements.txt` – Python dependencies
- `config.py` – configuration settings loaded from `.env`
- `.env` – environment values for local execution

### Data Pipeline
- `data_pipeline/main/main.py` – Prefect flow orchestrating all collection and analysis tasks
- `data_pipeline/main/deploy.py` – Prefect deployment definition / schedule
- `data_pipeline/database/connection.py` – Postgres connection pool using `ThreadedConnectionPool`
- `data_pipeline/database/schema.sql` – database schema for all tables
- `data_pipeline/collectors/`
  - `prices.py` – fetches historical price data with `yfinance`
  - `news.py` – fetches company news from Finnhub
  - `fundamentals.py` – pulls raw fundamentals from Finnhub
  - `insider_transactions.py` – loads insider trade filings
  - `peers.py` – loads company peer tickers
  - `analyze_news.py` – runs sentiment analysis on news content using `transformers`

### Dashboard
- `dashboard/Home.py` – main Streamlit landing page
- `dashboard/pages/1_Stock_Analysis.py` – individual stock deep dive
- `dashboard/pages/2_Sector_Overview.py` – cross-stock comparison view
- `dashboard/loader.py` – data-loader helpers for dashboard pages
- `dashboard/signals.py` – derives trend and health scores

### Testing / Drafts
- `testing/` – notebook drafts and experimental code

## Technologies Used

- Python
- Streamlit
- Prefect
- Postgres (`psycopg2-binary`)
- Finnhub API
- yfinance
- Transformers (`ProsusAI/finbert`)
- Pandas / NumPy
- Plotly
- Pydantic settings
- GitHub Actions workflow for scheduled pipeline runs

## Key Components

### Configuration
- `config.py` defines application settings
- loads values from `.env`
- includes watchlist, API keys, date ranges, and collection periods

### Database
- `data_pipeline/database/connection.py` provides connection pooling
- `data_pipeline/database/schema.sql` declares tables for:
  - `stocks`
  - `prices`
  - `news_articles`
  - `insider_transactions`
  - `stock_peers`
  - `raw_stock_fundamentals`
  - `social_posts`
  - `analysis_results`

### Data Collection
The pipeline collects data through Prefect tasks:
- `collect_prices`
- `collect_news`
- `collect_raw_fundemantals`
- `collect_insider_transactions`
- `collect_peers`
- `analyze_news_articles`

`data_pipeline/main/main.py` runs these tasks for each ticker in the watchlist.

### Dashboard
The Streamlit app renders:
- watchlist metrics
- price charts
- sentiment history
- recent news
- fundamentals and insider transaction summaries
- sector-level signal and health comparison

Dashboard loaders read from the Postgres database and use `get_connection()` / `put_connection()`.

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt