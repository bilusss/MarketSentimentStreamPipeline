CREATE TABLE IF NOT EXISTS crypto_prices (
  id SERIAL PRIMARY KEY,
  symbol VARCHAR(10),
  price FLOAT,
  quantity FLOAT,
  trade_time TIMESTAMPTZ,
  received_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS news_sentiment (
  id SERIAL PRIMARY KEY,
  title TEXT,
  source VARCHAR(100),
  url TEXT,
  sentiment VARCHAR(20),
  sentiment_score FLOAT,
  published_at TIMESTAMPTZ,
  fetched_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sentiment_price_snapshot (
  id SERIAL PRIMARY KEY,
  symbol VARCHAR(20),
  price FLOAT,
  avg_sentiment_score FLOAT,
  dominant_sentiment VARCHAR(20),
  news_count INT,
  alert BOOLEAN,
  alert_reason TEXT,
  snapshot_time TIMESTAMPTZ DEFAULT NOW()
);