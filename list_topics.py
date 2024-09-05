from kafka.admin import KafkaAdminClient

def list_kafka_topics():
    # Create a KafkaAdminClient to interact with Kafka
    admin_client = KafkaAdminClient(
        bootstrap_servers='kafka:9092',  # Replace with your Kafka broker address
        client_id='list-topics-client'
    )

    # Fetch the list of topics
    topics = admin_client.list_topics()

    print("Kafka Topics:")
    for topic in topics:
        print(f"- {topic}")

    admin_client.close()

if __name__ == "__main__":
    list_kafka_topics()