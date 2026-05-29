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

@flow(
    name="Collecting Data",
    task_runner=ConcurrentTaskRunner(1),
    log_prints=True
)
def data_pipeline(watchlist):
    # conn = get_connection()
    for ticker in watchlist:
        f_prices = collect_prices.submit(ticker=ticker,period=settings.prices_collection_period)
        f_peers = collect_peers.submit(ticker, finnhub_client)
        f_fundamentels = collect_raw_fundemantals.submit(ticker, finnhub_client)
        f_insider_trans = collect_insider_transactions.submit(ticker, settings.insider_trans_from, settings.insider_trans_to, finnhub_client)
        f_news = collect_news.submit(ticker, settings.news_from, settings.news_to, finnhub_client)
        f_analyze_news = analyze_news_articles.submit(ticker, settings.analyze_news_published_at, wait_for=[f_news])


if __name__ == "__main__":
    conn = get_connection()
    conn.rollback()
    put_connection(conn)
    data_pipeline(watchlist=settings.watchlist)

