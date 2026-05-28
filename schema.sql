--
-- PostgreSQL database dump
--

\restrict AySeJPXkRS64CSfrgonJQcghDfEGG40id4y5kYihksqDO0kjrjvQsSKfBTMOb0h

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: analysis_results; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.analysis_results (
    id integer NOT NULL,
    ticker character varying(10),
    analysis_date date,
    sentiment_score numeric(4,2),
    trend_signal character varying(10),
    reasoning text,
    health_score numeric(4,2),
    raw_response jsonb,
    created_at timestamp without time zone DEFAULT now()
);


--
-- Name: analysis_results_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.analysis_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: analysis_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.analysis_results_id_seq OWNED BY public.analysis_results.id;


--
-- Name: insider_trans; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.insider_trans (
    id integer NOT NULL,
    ticker character varying(10),
    change numeric(10,2),
    name character varying(40),
    filingdate date NOT NULL,
    transdate date NOT NULL,
    share numeric(10,2),
    transcode character varying(10),
    transprice numeric(10,2)
);


--
-- Name: insider_trans_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.insider_trans_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: insider_trans_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.insider_trans_id_seq OWNED BY public.insider_trans.id;


--
-- Name: news_articles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.news_articles (
    id integer NOT NULL,
    ticker character varying(10),
    headline text NOT NULL,
    source character varying(100),
    url text,
    published_at timestamp without time zone,
    raw_content text,
    scraped_at timestamp without time zone DEFAULT now(),
    label character varying(10),
    score double precision
);


--
-- Name: news_articles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.news_articles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: news_articles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.news_articles_id_seq OWNED BY public.news_articles.id;


--
-- Name: prices; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.prices (
    id integer NOT NULL,
    ticker character varying(10),
    date date NOT NULL,
    open numeric(10,2),
    high numeric(10,2),
    low numeric(10,2),
    close numeric(10,2),
    volume bigint
);


--
-- Name: prices_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.prices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: prices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.prices_id_seq OWNED BY public.prices.id;


--
-- Name: raw_stock_fundamentals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_stock_fundamentals (
    id integer NOT NULL,
    curated_at timestamp without time zone DEFAULT now(),
    payload jsonb,
    ticker character varying(10)
);


--
-- Name: raw_stock_fundamentals_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.raw_stock_fundamentals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: raw_stock_fundamentals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.raw_stock_fundamentals_id_seq OWNED BY public.raw_stock_fundamentals.id;


--
-- Name: social_posts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.social_posts (
    id integer NOT NULL,
    ticker character varying(10),
    platform character varying(20),
    post_id character varying(100),
    content text,
    score integer,
    author character varying(100),
    posted_at timestamp without time zone,
    scraped_at timestamp without time zone DEFAULT now()
);


--
-- Name: social_posts_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.social_posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: social_posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.social_posts_id_seq OWNED BY public.social_posts.id;


--
-- Name: stock_peers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stock_peers (
    ticker text NOT NULL,
    peer_ticker text NOT NULL
);


--
-- Name: stocks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stocks (
    ticker character varying(10) NOT NULL,
    name character varying(100),
    sector character varying(50),
    added_at timestamp without time zone DEFAULT now()
);


--
-- Name: analysis_results id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.analysis_results ALTER COLUMN id SET DEFAULT nextval('public.analysis_results_id_seq'::regclass);


--
-- Name: insider_trans id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insider_trans ALTER COLUMN id SET DEFAULT nextval('public.insider_trans_id_seq'::regclass);


--
-- Name: news_articles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.news_articles ALTER COLUMN id SET DEFAULT nextval('public.news_articles_id_seq'::regclass);


--
-- Name: prices id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prices ALTER COLUMN id SET DEFAULT nextval('public.prices_id_seq'::regclass);


--
-- Name: raw_stock_fundamentals id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_stock_fundamentals ALTER COLUMN id SET DEFAULT nextval('public.raw_stock_fundamentals_id_seq'::regclass);


--
-- Name: social_posts id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.social_posts ALTER COLUMN id SET DEFAULT nextval('public.social_posts_id_seq'::regclass);


--
-- Name: analysis_results analysis_results_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.analysis_results
    ADD CONSTRAINT analysis_results_pkey PRIMARY KEY (id);


--
-- Name: insider_trans insider_trans_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insider_trans
    ADD CONSTRAINT insider_trans_pkey PRIMARY KEY (id);


--
-- Name: news_articles news_articles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.news_articles
    ADD CONSTRAINT news_articles_pkey PRIMARY KEY (id);


--
-- Name: news_articles news_articles_url_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.news_articles
    ADD CONSTRAINT news_articles_url_key UNIQUE (url);


--
-- Name: prices prices_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prices
    ADD CONSTRAINT prices_pkey PRIMARY KEY (id);


--
-- Name: prices prices_ticker_date_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prices
    ADD CONSTRAINT prices_ticker_date_key UNIQUE (ticker, date);


--
-- Name: raw_stock_fundamentals raw_stock_fundamentals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_stock_fundamentals
    ADD CONSTRAINT raw_stock_fundamentals_pkey PRIMARY KEY (id);


--
-- Name: social_posts social_posts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.social_posts
    ADD CONSTRAINT social_posts_pkey PRIMARY KEY (id);


--
-- Name: social_posts social_posts_post_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.social_posts
    ADD CONSTRAINT social_posts_post_id_key UNIQUE (post_id);


--
-- Name: stock_peers stock_peers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_peers
    ADD CONSTRAINT stock_peers_pkey PRIMARY KEY (ticker, peer_ticker);


--
-- Name: stocks stocks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stocks
    ADD CONSTRAINT stocks_pkey PRIMARY KEY (ticker);


--
-- Name: prices unique_ticker_date; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prices
    ADD CONSTRAINT unique_ticker_date UNIQUE (ticker, date);


--
-- Name: analysis_results analysis_results_ticker_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.analysis_results
    ADD CONSTRAINT analysis_results_ticker_fkey FOREIGN KEY (ticker) REFERENCES public.stocks(ticker);


--
-- Name: insider_trans insider_trans_ticker_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insider_trans
    ADD CONSTRAINT insider_trans_ticker_fkey FOREIGN KEY (ticker) REFERENCES public.stocks(ticker);


--
-- Name: news_articles news_articles_ticker_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.news_articles
    ADD CONSTRAINT news_articles_ticker_fkey FOREIGN KEY (ticker) REFERENCES public.stocks(ticker);


--
-- Name: prices prices_ticker_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prices
    ADD CONSTRAINT prices_ticker_fkey FOREIGN KEY (ticker) REFERENCES public.stocks(ticker);


--
-- Name: raw_stock_fundamentals raw_stock_fundamentals_ticker_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_stock_fundamentals
    ADD CONSTRAINT raw_stock_fundamentals_ticker_fkey FOREIGN KEY (ticker) REFERENCES public.stocks(ticker);


--
-- Name: social_posts social_posts_ticker_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.social_posts
    ADD CONSTRAINT social_posts_ticker_fkey FOREIGN KEY (ticker) REFERENCES public.stocks(ticker);


--
-- Name: stock_peers stock_peers_peer_ticker_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_peers
    ADD CONSTRAINT stock_peers_peer_ticker_fkey FOREIGN KEY (peer_ticker) REFERENCES public.stocks(ticker);


--
-- Name: stock_peers stock_peers_ticker_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_peers
    ADD CONSTRAINT stock_peers_ticker_fkey FOREIGN KEY (ticker) REFERENCES public.stocks(ticker);


--
-- PostgreSQL database dump complete
--

\unrestrict AySeJPXkRS64CSfrgonJQcghDfEGG40id4y5kYihksqDO0kjrjvQsSKfBTMOb0h

