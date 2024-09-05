# delivery_service.py

from kafka import KafkaConsumer, KafkaProducer
import json
import time
from kafka.errors import NoBrokersAvailable

def track_delivery():
    consumer = None
    while not consumer:
        try:
            consumer = KafkaConsumer(
                'payment_topic',
                bootstrap_servers='kafka:9092',
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
        except NoBrokersAvailable:
            print("Kafka broker not available yet, retrying in 5 seconds...")
            time.sleep(5)  # Wait and retry

    producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    for message in consumer:
        order = message.value
        print(f"Starting delivery for order: {order['order_id']}")
        order['status'] = 'Out for Delivery'
        producer.send('delivery_topic', order)
        print(f"Delivery started for: {order['order_id']}")
        producer.flush()

if __name__ == "__main__":
    track_delivery()
