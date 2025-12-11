import json
import time
import argparse
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from generator import generate_reading

TOPIC = "quality_data"

def create_topic_if_missing(bootstrap_servers):
    admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers, client_id="admin-client")
    existing = admin.list_topics()
    if TOPIC not in existing:
        topic = NewTopic(name=TOPIC, num_partitions=1, replication_factor=1)
        admin.create_topics([topic])
        print(f"Created topic {TOPIC}")
    admin.close()

def main(brokers, interval):
    create_topic_if_missing(brokers)
    producer = KafkaProducer(
        bootstrap_servers=brokers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        linger_ms=10
    )
    print("Producer started. Press Ctrl-C to stop.")
    try:
        while True:
            reading = generate_reading()
            producer.send(TOPIC, value=reading)
            print("Sent:", reading)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Stopping producer...")
    finally:
        producer.flush()
        producer.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quality data producer")
    parser.add_argument("--brokers", default="localhost:9092")
    parser.add_argument("--interval", type=float, default=1.0)
    args = parser.parse_args()
    main(args.brokers, args.interval)
