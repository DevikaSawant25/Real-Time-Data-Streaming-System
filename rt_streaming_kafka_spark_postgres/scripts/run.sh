#!/usr/bin/env bash
set -e
docker compose up -d zookeeper kafka postgres adminer
echo "Waiting 15s for services..."; sleep 15
docker compose up -d producer
docker compose up -d spark
echo "Adminer at http://localhost:8081  (System: PostgreSQL, Server: postgres, user: postgres, pass: postgres, DB: analytics)"
