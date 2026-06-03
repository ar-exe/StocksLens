import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import logging
from data_pipeline.collectors.prices import collect_prices
from data_pipeline.collectors.peers import collect_peers
from data_pipeline.collectors.news import collect_news
from data_pipeline.collectors.fundamentals import collect_raw_fundemantals
from data_pipeline.collectors.insider_transactions import collect_insider_transactions
from data_pipeline.collectors.analyze_news import analyze_news_articles
from data_pipeline.database.connection import get_connection, put_connection
import finnhub
from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner
from prefect.tasks import task_input_hash
from datetime import timedelta
from config import settings
from prefect.task_runners import ThreadPoolTaskRunner
finnhub_client = finnhub.Client(api_key=settings.finnhub_key)
@task
def join(*args):
    return True
@flow(
    name="Collecting Data",
    task_runner=ConcurrentTaskRunner(1),
    log_prints=True
)
def data_pipeline(watchlist):
    # conn = get_connection()
    for ticker in watchlist:
        try:
            f_prices = collect_prices(ticker=ticker,period=settings.prices_collection_period)
            f_peers = collect_peers(ticker, finnhub_client)
            f_fundamentels = collect_raw_fundemantals(ticker, finnhub_client)
            f_insider_trans = collect_insider_transactions(ticker, settings.insider_trans_from, settings.insider_trans_to, finnhub_client)
            f_news = collect_news(ticker, settings.news_from, settings.news_to, finnhub_client)
            f_analyze_news = analyze_news_articles(ticker, settings.analyze_news_published_at, wait_for=[f_news])
            end = join.submit(
                f_prices,
                f_peers,
                f_fundamentels,
                f_insider_trans,
                f_news,
                f_analyze_news,
            )
            end.result()
        except Exception as e:
            print(f"❌ Error processing {ticker}: {e}")
            raise  # or continue to skip failed tickers

if __name__ == "__main__":
    conn = get_connection()
    conn.rollback()
    put_connection(conn)
    data_pipeline(watchlist=settings.watchlist)

