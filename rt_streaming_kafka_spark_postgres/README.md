# Real-Time Data Streaming System (Kafka + Spark Structured Streaming + PostgreSQL)

## Overview
- Python **producer** streams realistic clickstream JSON events to Kafka topic `clickstream`.
- **Spark Structured Streaming** consumes Kafka, cleans/deduplicates, writes:
  - Raw events → `clickstream_events` (Postgres)
  - 1-minute URL aggregates → `clickstream_agg_minute` (Postgres)
- Use **Adminer** at http://localhost:8081 to query results.

## Run
```bash
./scripts/run.sh
# Or:
# docker compose up -d zookeeper kafka postgres adminer
# docker compose up -d producer
# docker compose up -d spark
```

## DB access
Adminer: http://localhost:8081  
System: PostgreSQL, Server: postgres, User: postgres, Password: postgres, DB: analytics

## Files
- `docker-compose.yml` — all services
- `sql/init.sql` — creates tables
- `app/producer/producer.py` — Kafka producer (uses `kafka-python` + `faker`)
- `app/spark_streaming_job.py` — Spark job (Kafka source → Postgres sinks)
- `scripts/run.sh`, `scripts/stop.sh` — helpers

## Notes
- Spark picks up Kafka & Postgres packages via `--packages` in compose.
- Checkpoints at `/tmp/chk_*` inside the Spark container (persist across restarts unless container removed).
- Tweak producer rate with `RATE_PER_SEC` in compose.
