# kafka_listener.py

from kafka import KafkaConsumer
import json

def listen_to_topic(topic_name):
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print(f"Listening to Kafka topic: {topic_name}")

    for message in consumer:
        print(f"Message: {message.value}")

if __name__ == "__main__":
    listen_to_topic('order_topic')
