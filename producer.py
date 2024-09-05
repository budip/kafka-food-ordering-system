from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import time
import sys

# Function to produce messages to Kafka
def produce_messages(num_messages=None):
    producer = None
    while not producer:
        try:
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
        except NoBrokersAvailable:
            print("Kafka broker not available, retrying...")
            time.sleep(1)

    message_count = 0
    while num_messages is None or message_count < num_messages:
        message = f"Message {message_count} from producer"
        producer.send('test-topic', message.encode('utf-8'))
        print(f"Sent: {message}")
        message_count += 1
        time.sleep(10)

    producer.flush()
    producer.close()

if __name__ == "__main__":
    num_messages = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    produce_messages(num_messages)