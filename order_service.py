# order_service.py

from kafka import KafkaProducer
import json
import time
from kafka.errors import NoBrokersAvailable

def place_order(order_id, customer_name, items):
    producer = None
    while not producer:
        try:
            producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        except NoBrokersAvailable:
            print("Kafka broker not available yet, retrying in 5 seconds...")
            time.sleep(5)  # Wait and retry
    order = {"order_id": order_id, "customer_name": customer_name, "items": items, "status": "Order Placed"}
    producer.send('order_topic', order)
    print(f"Order Placed: {order}")
    producer.flush()
    producer.close()

if __name__ == "__main__":
    # Simulate placing an order every 10 seconds
    order_id = 1
    while True:
        place_order(order_id, "Customer_" + str(order_id), ["Burger", "Fries"])
        order_id += 1
        time.sleep(10)
