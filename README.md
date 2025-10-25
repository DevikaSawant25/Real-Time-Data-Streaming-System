⚡ Real-Time Data Streaming System

Tech Stack: Apache Kafka | Spark Structured Streaming | PostgreSQL | Python | Docker

🧠 Overview

This project demonstrates a real-time clickstream data pipeline using
Apache Kafka and Spark Structured Streaming, with PostgreSQL as the analytical data store.
The system continuously ingests simulated user events from a Python producer,
processes them in real time with Spark, and writes both raw events and aggregated metrics into PostgreSQL for analytics dashboards.

Highlights

Sub-second stream ingestion and transformation
Real-time data aggregation and persistence
Fully containerized setup with Docker Compose
Fault-tolerant and replayable Kafka topic design

🧩 Architecture
flowchart LR
    A[Python Producer] -->|JSON Events| B[(Kafka Topic: clickstream)]
    B -->|Structured Streaming| C[Spark Streaming Job]
    C -->|Write Raw Events| D[(PostgreSQL - clickstream_events)]
    C -->|Aggregate 1-min Windows| E[(PostgreSQL - clickstream_agg_minute)]
    E --> F[PowerBI / Grafana Analytics]

⚙️ Core Features

✅ Real-time Ingestion: Simulated user activity streamed via Kafka Producer
✅ Event Processing: Spark Structured Streaming for ETL & window aggregation
✅ Data Persistence: PostgreSQL for storing both raw and aggregated data
✅ Streaming Analytics: Minute-level traffic metrics for URLs and sessions
✅ Dockerized Infrastructure: Zookeeper, Kafka, Spark, Postgres, Adminer all in one stack

🧱 Pipeline Components
Component	Technology	Description
Data Producer	Python + kafka-python	Generates synthetic clickstream JSON events
Message Broker	Apache Kafka	Ensures distributed, reliable event streaming
Stream Processor	Apache Spark Structured Streaming	Parses, cleans, aggregates events in micro-batches
Database Sink	PostgreSQL	Stores processed raw and aggregated metrics
Visualization	PowerBI / Grafana	Displays real-time analytics dashboards
🧮 Data Model
🟣 Raw Table – clickstream_events
event_id	user_id	event_ts	url	referrer	ip	received_at
d7f3-91a2...	201	2025-10-25 09:12:10	/product/101	google.com	192.168.1.45	2025-10-25 09:12:11
🟢 Aggregated Table – clickstream_agg_minute
window_start	window_end	url	hits
2025-10-25 09:10:00	2025-10-25 09:11:00	/product/101	142
🧰 Setup Instructions
1️⃣ Clone & Configure
git clone https://github.com/DevikaSawant25/real-time-data-streaming.git
cd real-time-data-streaming
cp .env.example .env

2️⃣ Start the Services
docker compose up -d zookeeper kafka postgres adminer
docker compose up -d producer spark

3️⃣ Monitor in Adminer

Open http://localhost:8081
System: PostgreSQL
Server: postgres
User: postgres
Password: postgres
Database: analytics

🧪 Spark Processing Logic

Reads Kafka topic: clickstream
Parses JSON schema → validates fields
Cleans & deduplicates records by event_id
Writes results using foreachBatch() to PostgreSQL
Performs 1-minute aggregations with watermarks to handle late data

📈 Performance & Results

Achieved sub-second latency between ingestion and availability in PostgreSQL
Processed over 5K events/minute on a local setup
Delivered real-time visibility into product and page traffic trends

📦 Project Structure
rt-streaming/
├── app/
│   ├── producer/
│   │   └── producer.py
│   └── spark_streaming_job.py
├── sql/
│   └── init.sql
├── scripts/
│   ├── run.sh
│   └── stop.sh
├── docker-compose.yml
└── README.md

🧠 Key Learnings

Event-driven architectures with Kafka topics and partitions
Real-time data ETL with Spark Structured Streaming
Writing streaming data to relational databases safely
End-to-end orchestration and containerization using Docker

🏁 Future Enhancements

Integrate Prometheus + Grafana for stream monitoring
Add Flink / Kafka Streams comparison module
Deploy on AWS MSK + EMR + RDS for production scaling
