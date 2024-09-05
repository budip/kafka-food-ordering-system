# payment_service.py

from kafka import KafkaConsumer, KafkaProducer
import json
import time
from kafka.errors import NoBrokersAvailable

def process_payment():
    consumer = None
    while not consumer:
        try:
            consumer = KafkaConsumer(
                'order_topic',
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
        print(f"Processing payment for order: {order['order_id']}")
        order['status'] = 'Payment Processed'
        producer.send('payment_topic', order)
        print(f"Payment Processed: {order['order_id']}")
        producer.flush()

if __name__ == "__main__":
    process_payment()
