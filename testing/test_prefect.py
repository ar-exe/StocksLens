# from prefect import flow, task
# import time

# @task(name="Fetch prices")
# def fetch_prices(ticker: str) -> dict:
#     print(f"  fetching prices for {ticker}...")
#     time.sleep(1)  # simulating API call
#     return {"ticker": ticker, "close": 182.50}

# @task(name="Fetch news")
# def fetch_news(ticker: str) -> list:
#     print(f"  fetching news for {ticker}...")
#     time.sleep(1)
#     return [{"headline": f"Big news about {ticker}"}]

# @task(name="Analyze")
# def analyze(ticker: str, prices: dict, news: list) -> str:
#     print(f"  analyzing {ticker}...")
#     return f"BULLISH — close at {prices['close']}, {len(news)} articles"

# @flow(name="My first flow")
# def pipeline(ticker: str = "AAPL"):
#     prices = fetch_prices(ticker)   # runs, blocks, returns actual dict
#     news   = fetch_news(ticker)     # runs after prices finishes
#     result = analyze(ticker, prices, news)
#     print(f"Result: {result}")

# pipeline("AAPL")

from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner
import time

@task(name="Fetch prices")
def fetch_prices(ticker: str) -> dict:
    print(f"  fetching prices for {ticker}...")
    time.sleep(1)
    return {"ticker": ticker, "close": 182.50}

@task(name="Fetch news")
def fetch_news(ticker: str) -> list:
    print(f"  fetching news for {ticker}...")
    time.sleep(1)
    return [{"headline": f"Big news about {ticker}"}]

@task(name="Analyze")
def analyze(ticker: str, prices: dict, news: list) -> str:
    print(f"  analyzing {ticker}...")
    return f"BULLISH — close at {prices['close']}, {len(news)} articles"

@flow(
    name="My first flow",
    task_runner=ConcurrentTaskRunner()  # enables parallel execution
)
def pipeline(ticker: str = "AAPL"):
    # Submit both — they start immediately, run at the same time
    prices_future = fetch_prices.submit(ticker)
    news_future   = fetch_news.submit(ticker)

    # .result() blocks here until BOTH are done
    # Prefect sees you're passing futures into analyze —
    # it automatically waits for them before running analyze
    result = analyze(ticker, prices_future, news_future)

    print(f"Result: {result.result()}")

pipeline("AAPL")