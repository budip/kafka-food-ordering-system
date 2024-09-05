
## Setup Empty Container

### Step 1: Create a Dockerfile

In the project directory, create a Dockerfile:
<small><small>

```yaml
# Use the official Python image
FROM python:3.9-slim

# Set a working directory
WORKDIR /usr/src/app

# Optionally: Install additional dependencies
# RUN apt-get update && apt-get install -y some-package

# Default command to run a Python shell
CMD ["python3"]
```
</small></small>

### Step 2: Create a docker-compose.yml File
<small><small>

```yaml
services:
  python-app:
    build: .
    container_name: python3-container
    stdin_open: true  # Keep stdin open for interactive containers
    tty: true         # Allocate a pseudo-TTY for the container
```
</small></small>

### Step 3: Use Docker Compose to Build and Run the Service
Now, in your terminal, navigate to the directory where both the Dockerfile and docker-compose.yml are located, and run the following commands:

Build the Docker Image: <small>`docker-compose build`</small>

Run the Docker Container: <small>`docker-compose up`</small>

Access the container: <small>`docker exec -it python3-container`</small>

## Add Kafka Service
### Update docker-compose.yml file
<small><small>

```yaml
version: '3'
services:
  python-app:
    build: .
    container_name: python3-container
    stdin_open: true
    tty: true
    depends_on:
      - zookeeper
      - kafka

  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka:
    image: confluentinc/cp-kafka:latest
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    depends_on:
      - zookeeper
```
</small></small>

### Modify Dockerfile
<small><small>

```yaml
# Use the official Python image
FROM python:3.9-slim

# Set a working directory
WORKDIR /usr/src/app

# Copy the requirements file (if needed)
COPY requirements.txt .

# Install necessary Python libraries (including kafka-python)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script to the container
COPY hello.py .

# Command to run the Python script
CMD ["python3", "hello.py"]
```
</small></small>

### Add Kafka to requirements.txt
<small><small>

```bash
kafka-python
```
</small></small>

### Update hello.py to interact with Kafka
<small><small>

```python
# hello.py

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable
import time

# Produce a message to Kafka
def produce_message():
    producer = None
    while not producer:
        try:
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
        except NoBrokersAvailable:
            print("Kafka broker not available yet, retrying...")
            time.sleep(1)
    producer.send('test-topic', b'Hello from Python!')
    producer.flush()
    print("Message sent to Kafka!")

# Consume messages from Kafka
def consume_message():
    consumer = KafkaConsumer(
        'test-topic',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group')
    print("Waiting for messages...")
    for message in consumer:
        print(f"Received message: {message.value.decode('utf-8')}")
        break

if __name__ == "__main__":
    produce_message()
    consume_message()
```
</small></small>

Build and run the entire steps. You should see these messages in the log:
<small><small>

```log
python3-container | Message sent to Kafka!
python3-container | Waiting for messages...
python3-container | Received message: Hello from Python!
```
</small></small>

