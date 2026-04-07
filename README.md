# 📰 Market Sentiment Stream Pipeline

A real-time data pipeline designed to detect **divergence** between cryptocurrency price movements and financial news sentiment. The system synchronizes tick-by-tick data from **Binance WebSocket** and news headlines from **NewsAPI**, utilizing **Apache Kafka** as a high-throughput message broker.

---

## 🏗️ System Architecture

The system follows an **Event-Driven Architecture (EDA)**:
1.  **Producers**: Responsible for real-time data ingestion. 
    * *Price Producer*: Streams tick-by-tick data.
    * *News Producer*: Fetches headlines and performs **NLP inference** using **FinBERT**.
2.  **Broker (Kafka)**: Orchestrates data streams, ensuring decoupling between ingestion and processing layers.
3.  **Consumer**: Aggregates data within sliding time windows, detects price-sentiment anomalies, and persists snapshots to **PostgreSQL**.
4.  **Dashboard (Streamlit)**: A front-end layer for live monitoring of market sentiment and automated divergence alerts.

---

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Streaming:** Apache Kafka (Confluent Platform)
* **NLP:** FinBERT (Hugging Face Transformers)
* **Database:** PostgreSQL 17
* **Visualization:** Streamlit & Plotly
* **Containerization:** Docker & Docker Compose
* **Libraries:** SQLAlchemy, Pandas, WebSocket-client, PyTorch

---

## 📂 Project Structure

```text
crypto-sentiment-pipeline/
├── core/
│   ├── logging_config.py   # Centralized logging configuration
│   ├── sentiment.py        # NLP Analysis Logic (FinBERT)
│   └── divergence.py       # Divergence detection algorithms
├── producers/
│   ├── price_producer.py   # Binance WebSocket -> Kafka
│   └── news_producer.py    # NewsAPI -> Sentiment Analysis -> Kafka
├── consumer/
│   └── consumer.py         # Kafka Stream Processing -> PostgreSQL
├── dashboard/
│   └── app.py              # Streamlit Live Dashboard
├── database/
│   └── schema.sql          # SQL Schema & Table definitions
├── tests/                  # Unit and Integration test suites
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## 🚀 Project Roadmap

### 🟢 FOUNDATION
- [ ] Logger setup (`core/logger.py`)
- [ ] Database schema design (`database/schema.sql`)
- [ ] Docker-compose orchestration (`docker-compose.yml`)
- [ ] Environment configuration (`.env`, `.env.example`)
- [ ] Requirements specification

### 🟡 CORE LOGIC
- [ ] Sentiment analysis module (`core/sentiment.py`)
- [ ] Divergence detection engine (`core/divergence.py`)

### 🔵 COMPONENTS
- [ ] **Price Producer**: Binance WebSocket integration
- [ ] **News Producer**: NewsAPI + FinBERT integration
- [ ] **Consumer Pipeline**: Stream merging and snapshot persistence
- [ ] **Streamlit Dashboard**: Real-time visualization (IN PROGRESS)

### 🔴 QUALITY & GO LIVE
- [ ] Unit tests (Sentiment & Divergence modules)
- [ ] Integration tests for the full pipeline
- [ ] Alert monitoring (False Positive mitigation)
- [ ] Threshold tuning for production-ready alerts

---

## 🔧 Quick Start

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/biluss/MarketSentimentStreamPipeline.git
    cd MarketSentimentStreamPipeline
    ```

2.  **Spin up the infrastructure:**
    ```bash
    docker-compose up -d
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Launch components (in separate terminals):**
    ```bash
    # 1. Start the consumer to prepare the database
    python consumer/consumer.py

    # 2. Start data producers
    python producers/price_producer.py
    python producers/news_producer.py

    # 3. Launch the monitoring UI
    streamlit run dashboard/app.py
    ```
