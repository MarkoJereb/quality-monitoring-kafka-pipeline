import json
import argparse
from kafka import KafkaConsumer
from utils.schema import validate_message
from db import PostgresClient

TOPIC = "quality_data"

THRESHOLDS = {
    "temperature": (0, 30),
    "ph": (3, 8),
    "moisture": (10, 80)
}

def check_alerts(rec):
    alerts = []
    for k, (low, high) in THRESHOLDS.items():
        val = rec.get(k)
        if val < low or val > high:
            alerts.append(k)
    return alerts

def main(brokers, dsn):
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=brokers,
        value_deserializer=lambda b: json.loads(b.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        consumer_timeout_ms=1000
    )
    db = PostgresClient(dsn)
    print("Consumer started.")
    try:
        while True:
            for msg in consumer:
                rec = msg.value
                validate_message(rec)
                alerts = check_alerts(rec)
                flag = bool(alerts)
                db.insert_reading(rec["ts"], rec["temperature"], rec["ph"], rec["moisture"], flag)
                print("Stored:", rec, "Alert:", flag)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--brokers", default="localhost:9092")
    parser.add_argument("--dsn", default="postgresql://pq_user:pq_pass@localhost:5432/qualitydb")
    args = parser.parse_args()
    main(args.brokers, args.dsn)
