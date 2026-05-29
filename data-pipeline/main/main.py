import logging
from collectors.prices import collect_prices
from collectors.peers import collect_peers
from collectors.news import collect_news
from collectors.fundamentals import collect_raw_fundemantals
from collectors.insider_transactions import collect_insider_transactions
from collectors.analyze_news import analyze_news_articles
from database.connection import get_connection

from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner
from prefect.tasks import task_input_hash
from datetime import timedelta

@flow(
    name="Collecting Data",
    task_runner=ConcurrentTaskRunner(),
    log_prints=True
)
def data_pipeline(watchlist):
    conn = get_connection()
    for ticker in watchlist:
        f_prices = collect_prices(ticker=ticker,period=period, conn=conn)
        f_peers = collect_peers(ticker, finnhub_client, conn)
        f_fundamentels = collect_raw_fundemantals(ticker, finnhub_client, conn)
        f_insider_trans = collect_insider_transactions(ticker, dfrom, dto, finnhub_client, conn)
        f_news = collect_news(ticker, dfrom, dto, finnhub_client, conn)
        f_analyze_news = analyze_news_articles(ticker, published_at, classifier, conn)


if __name__ == "__main__":
    watchlist = 
    data_pipeline(watchlist=watchlist)

