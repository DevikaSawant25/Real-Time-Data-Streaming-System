import os
import time
import json
import random
from datetime import datetime, timezone
from faker import Faker
from kafka import KafkaProducer

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = os.getenv("TOPIC_NAME", "clickstream")
RATE = float(os.getenv("RATE_PER_SEC", "5"))

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    linger_ms=50,
    acks="all",
    retries=5,
)

URLS = [
    "/",
    "/home",
    "/product/1001",
    "/product/1002",
    "/product/2001",
    "/cart",
    "/checkout",
    "/search?q=shoes",
    "/search?q=laptop",
]

def make_event():
    now = datetime.now(timezone.utc).isoformat()
    return {
        "event_id": fake.uuid4(),
        "user_id": str(random.randint(1, 5000)),
        "ts": now,
        "url": random.choice(URLS),
        "referrer": random.choice(["", "https://google.com", "https://twitter.com", "https://instagram.com"]),
        "ua": fake.user_agent(),
        "ip": fake.ipv4_public(),
    }

def main():
    print(f"Producing to {BOOTSTRAP} topic={TOPIC} at ~{RATE} eps")
    interval = 1.0 / RATE if RATE > 0 else 0.2
    while True:
        evt = make_event()
        producer.send(TOPIC, evt)
        time.sleep(interval)

if __name__ == "__main__":
    main()
