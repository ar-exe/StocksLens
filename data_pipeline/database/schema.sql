-- -- =========================================
-- STOCKS
-- =========================================

CREATE TABLE stocks (
    ticker VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    sector VARCHAR(50),
    added_at TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- PRICES
-- =========================================

CREATE TABLE prices (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,

    open NUMERIC(10,2),
    high NUMERIC(10,2),
    low NUMERIC(10,2),
    close NUMERIC(10,2),

    volume BIGINT,

    CONSTRAINT fk_prices_ticker
        FOREIGN KEY (ticker)
        REFERENCES stocks(ticker),

    CONSTRAINT uq_prices_ticker_date
        UNIQUE (ticker, date)
);

CREATE INDEX idx_prices_ticker_date
ON prices(ticker, date);

-- =========================================
-- NEWS ARTICLES
-- =========================================

CREATE TABLE news_articles (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    ticker VARCHAR(10) NOT NULL,

    headline TEXT NOT NULL,
    source VARCHAR(100),

    url TEXT UNIQUE,

    published_at TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT NOW(),

    raw_content TEXT,

    label VARCHAR(10),
    score DOUBLE PRECISION,

    CONSTRAINT fk_news_ticker
        FOREIGN KEY (ticker)
        REFERENCES stocks(ticker)
);

CREATE INDEX idx_news_ticker
ON news_articles(ticker);

CREATE INDEX idx_news_published_at
ON news_articles(published_at);

-- =========================================
-- INSIDER TRANSACTIONS
-- =========================================

CREATE TABLE insider_transactions (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    ticker VARCHAR(10) NOT NULL,

    name VARCHAR(40),

    filing_date DATE NOT NULL,
    transaction_date DATE NOT NULL,

    change_amount NUMERIC(10,2),
    shares NUMERIC(10,2),

    transaction_code VARCHAR(10),
    transaction_price NUMERIC(10,2),

    CONSTRAINT fk_insider_ticker
        FOREIGN KEY (ticker)
        REFERENCES stocks(ticker)
);

CREATE INDEX idx_insider_ticker
ON insider_transactions(ticker);

-- =========================================
-- STOCK PEERS
-- =========================================

CREATE TABLE stock_peers (
    ticker VARCHAR(10) NOT NULL,
    peer_ticker VARCHAR(10) NOT NULL,

    PRIMARY KEY (ticker, peer_ticker),

    CONSTRAINT fk_stock_peers_ticker
        FOREIGN KEY (ticker)
        REFERENCES stocks(ticker),

    CONSTRAINT fk_stock_peers_peer
        FOREIGN KEY (peer_ticker)
        REFERENCES stocks(ticker)
);

-- =========================================
-- RAW FUNDAMENTALS
-- =========================================

CREATE TABLE raw_stock_fundamentals (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    ticker VARCHAR(10) NOT NULL,

    payload JSONB,

    curated_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT fk_fundamentals_ticker
        FOREIGN KEY (ticker)
        REFERENCES stocks(ticker)
);

CREATE INDEX idx_fundamentals_ticker
ON raw_stock_fundamentals(ticker);

-- =========================================
-- SOCIAL POSTS
-- =========================================

CREATE TABLE social_posts (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    ticker VARCHAR(10) NOT NULL,

    platform VARCHAR(20),
    post_id VARCHAR(100) UNIQUE,

    content TEXT,

    score INTEGER,

    author VARCHAR(100),

    posted_at TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT fk_social_ticker
        FOREIGN KEY (ticker)
        REFERENCES stocks(ticker)
);

CREATE INDEX idx_social_ticker
ON social_posts(ticker);

-- =========================================
-- ANALYSIS RESULTS
-- =========================================

CREATE TABLE analysis_results (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    ticker VARCHAR(10) NOT NULL,

    analysis_date DATE,

    sentiment_score NUMERIC(4,2),
    health_score NUMERIC(4,2),

    trend_signal VARCHAR(10),

    reasoning TEXT,

    raw_response JSONB,

    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT fk_analysis_ticker
        FOREIGN KEY (ticker)
        REFERENCES stocks(ticker)
);

CREATE INDEX idx_analysis_ticker
ON analysis_results(ticker);