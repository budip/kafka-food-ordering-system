from kafka import KafkaConsumer

def inspect_kafka_topic(topic_name):
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',  # Read all messages from the beginning
        enable_auto_commit=False,      # Do not commit offsets to keep reading the same messages
        group_id=None                  # No consumer group, read all messages without tracking
    )

    print(f"Inspecting Kafka topic: {topic_name}")
    
    for message in consumer:
        print(f"Offset: {message.offset}, Message: {message.value.decode('utf-8')}")
        
    consumer.close()

if __name__ == "__main__":
    inspect_kafka_topic('test-topic')