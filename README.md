# Food Ordering System with Kafka

## Overview

This is a simple **Food Ordering System** built using **Apache Kafka** for inter-service communication. The system consists of three microservices:
<small>

- **Order Service** : Handles customer orders.
- **Payment Service** : Processes payments for the orders.
- **Delivery Service** : Manages the delivery of orders.
</small>

Each service communicates with the others asynchronously via Kafka topics, ensuring that the system remains scalable and decoupled.

#### Kafka Topics
<small>

- _order_topic_ : Handles new food orders.
- _payment_topic_ : Manages payment processing events.
- _delivery_topic_ : Manages delivery status updates.
</small>

#### Project Structure
<small><small>

```bash
/food-ordering-system
  ├── Dockerfile             # Docker setup for all services
  ├── docker-compose.yml     # Defines services and Kafka configuration
  ├── requirements.txt       # Python dependencies (Kafka Python client)
  ├── order_service.py       # Handles customer orders
  ├── payment_service.py     # Processes payments
  ├── delivery_service.py    # Manages delivery logistics
  └── kafka_listener.py      # Optional: Script to inspect Kafka topics
```
</small></small>

## Services
##### Order Service
<small>

- Places customer orders in the _order_topic_ Kafka topic.
- Runs continuously and places a new order every 10 seconds.
</small>

#### Payment Service
<small>

- Listens to the _order_topic_ and processes payments for new orders.
- Sends payment confirmation to the _payment_topic_.
</small>

#### Delivery Service
<small>

- Listens to the _payment_topic_ and manages the delivery of paid orders.
- Sends delivery status updates to the _delivery_topic_.
</small>

#### Optional
<small>

- Kafka Listener: _kafka_listener.py_ can be used to inspect any Kafka topic and print messages to the console.
</small>

## Requirements
- Docker
- Docker Compose
- kafka-python client


## Setup

### Step 1: Clone the Repository
<small><small>

```bash
git clone <repository-url>
cd food-ordering-system
```
</small></small>

### Step 2: Build the Docker Images
<small><small>

```bash
docker-compose build
```
</small></small>

### Step 3: Start Kafka, Zookeeper, and All Services

Start the Kafka broker, Zookeeper, and all three services (Order, Payment, and Delivery services) using Docker Compose:
docker-compose up

This will:
<small>

- Start the Zookeeper and Kafka services.
- Start the Order Service, which will place new orders.
- Start the Payment Service, which will listen for new orders and process payments.
- Start the Delivery Service, which will listen for payments and manage deliveries.
</small>

### Step 4: View Logs

To see how messages flow between services, you can check the logs for each service:
<small><small>

```bash
docker-compose logs order-service
docker-compose logs payment-service
docker-compose logs delivery-service
```
</small></small>

### Step 5: Inspect Kafka Topics (Optional)

You can use the provided _kafka_listener.py_ script to inspect any Kafka topic. For example, to inspect order_topic:
<small><small>

```bash
docker exec -it order-service python3 kafka_listener.py
```
</small></small>

### Step 6: Stop the Services

To stop all running services, use:
<small><small>

```bash
docker-compose down
```
</small></small>

## How It Works
<small>

- Order Service places an order, sending a message to the _order_topic_ Kafka topic.
- Payment Service listens to the _order_topic_ and processes the payment for new orders. After processing, it sends a message to the _payment_topic_.
- Delivery Service listens to the _payment_topic_, starts the delivery, and sends updates to the _delivery_topic_.
</small>

Example Flow:
<small>

- A new order is placed (e.g., _“Customer_1 ordered Burger and Fries”_).
- Payment Service processes the payment.
- Delivery Service starts delivering the order and updates the status.
</small>

#### Notes
<small>

-	The retry logic in all services ensures that the services keep trying to connect to Kafka if it’s not available immediately.
-	Kafka is used to decouple the services, allowing them to scale independently and handle asynchronous events.
</small>

#### Customization
<small>

- You can modify the _order_service.py_, _payment_service.py_, or _delivery_service.py_ scripts to adjust the behavior (e.g., frequency of orders, additional order details, etc.).
- You can add more services or Kafka topics as needed to extend the functionality.
</small>

## Troubleshooting
<small>

- If you see ***NoBrokersAvailable*** errors, it means the services can’t connect to Kafka. Ensure that Kafka is running and that the services are correctly configured to connect.
- Use docker-compose logs kafka to inspect the Kafka broker logs for further details.
</small>

## Support and Updates

If you encounter any issues, find missing components, or want to request updates, please reach out to bpchen@gmail.com.

## License

This project is open-source and licensed under the MIT License.
