from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import time
import sys

# Function to consume messages from Kafka
def consume_messages(topic_name, num_messages=None):
    consumer = None
    while not consumer:
        try:
            consumer = KafkaConsumer(
                topic_name,
                bootstrap_servers='kafka:9092',
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='consumer-group'
            )
        except NoBrokersAvailable:
            print("Kafka broker not available, retrying...")
            time.sleep(1)
    
    print(f"Listening to Kafka topic: {topic_name}")

    message_count = 0
    for message in consumer:
        print(f"Received message: {message.value.decode('utf-8')}")
        message_count += 1

        if num_messages is not None and message_count >= num_messages:
            break

    print(f"Consumed {message_count} messages.")
    consumer.close()

if __name__ == "__main__":
    num_messages = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    consume_messages('test-topic', num_messages)