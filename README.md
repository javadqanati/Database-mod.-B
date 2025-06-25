# Integration of MQTT Server and Python for Big Data Analysis and Storage in Different Database Platforms

**Database-mod.-B** is a modular database project designed to provide a foundational understanding of database management systems, their architecture, and implementation. This project aims to help students, developers, and enthusiasts explore the core principles of database systems, including data storage, indexing, query processing, and transaction management.

## Features

- **Modular Architecture:** Each component is organized into modules for easy understanding, extensibility, and maintainability.
- **Custom Storage Engine:** Implements basic data storage and retrieval mechanisms.
- **Indexing:** Supports simple indexing for efficient data access.
- **Query Processing:** Provides a framework for parsing and executing basic database queries.
- **Transaction Management:** Demonstrates fundamental concepts of transactions and concurrency control.
- **Educational Focus:** Well-documented code and examples to facilitate learning and experimentation.

## Description of the project:
The project aims to develop a system capable of collecting, processing and storing large volumes of data from sensors or IoT devices using the MQTT (Message Queuing Telemetry Transport) protocol and Python. 
The system will be able to manage the reception of data via MQTT server, analyze it in real time and store it in different types of databases, including SQL, MongoDB and Neo4j, based on the topic of the MQTT messages.


# System Architecture, Technologies Used, and Installation & Usage Instructions

## System Architecture Overview

**Database-mod.-B** is a modular, educational IoT data platform designed to demonstrate core concepts of database systems and their integration with real-time data pipelines. The system receives data from IoT devices or sensors via the MQTT protocol, processes it using Python, and stores it in various databases (MySQL, MongoDB, Neo4j) based on the data topic.

### Architectural Components

- **MQTT Broker**: Handles real-time data ingestion from sensors/IoT devices.
- **Python Subscriber**: Connects to the MQTT broker, processes incoming messages, and routes them to the appropriate database.
- **Databases**: 
  - **MySQL**: For structured temperature/time-series data.
  - **MongoDB**: For flexible, schema-less sensor data.
  - **Neo4j**: For graph-based relationships between users, devices, and sensors.
- **PHP Web Dashboard**: Provides a simple web interface to visualize stored data from all databases.

### Data Flow

1. IoT devices/simulators publish data to the MQTT broker under different topics.
2. Python subscriber listens to topics:
    - `temperature/` → stored in MySQL
    - `sensor/` → stored in MongoDB
    - `graph/` → stored in Neo4j
3. Data is stored and can be explored via the web dashboard.

---

## Technologies Used

- **Python**: Data ingestion (subscriber/publisher), database integration.
  - Libraries: `paho-mqtt`, `pymongo`, `py2neo`, `mysql-connector-python`
- **PHP (with Apache)**: Web dashboard with scripts for each database.
  - PHP extensions: PDO, MongoDB, Neo4j via Composer
- **Docker & Docker Compose**: Containerized deployment of all services.
- **Databases**: MySQL, MongoDB, Neo4j (all run as containers).
- **MQTT Broker**: Eclipse Mosquitto (containerized).

---

## Installation Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/javadqanati/Database-mod.-B.git
cd Database-mod.-B
```

### 2. Install Python Dependencies

For local development:
```sh
pip install -r subscriber/requirements.txt
```
Or, rely on Docker for full isolation (recommended).

### 3. Start the Databases and MQTT Broker

All main services—including MySQL, MongoDB, Neo4j, PHP Apache, and Mosquitto—can be launched using Docker Compose:

```sh
docker-compose build
docker-compose up
```

Alternatively, you can run just Mosquitto:
```sh
docker run -it -p 1883:1883 -p 9001:9001 eclipse-mosquitto
```

### 4. Start the Python MQTT Subscriber

Inside the container or your dev environment:
```sh
cd subscriber
python mqtt_subscriber.py
```

### 5. (Optional) Publish Simulated Data

To simulate IoT data, run the publisher:
```sh
python mqtt_publisher.py
```
Or:
```sh
python publisher.py
```
(depending on your setup)

### 6. Access the Web Dashboard

Navigate to `http://localhost:<apache_port>/php/index.php` (the port depends on your Docker Compose setup, usually 80 or 8080).

---

## Usage Instructions

- **View MySQL Data:** Click "MySQL Data" in the dashboard; shows recent temperature readings.
- **View MongoDB Data:** Click "Sensor Data (MongoDB)"; shows recent sensor entries.
- **View Neo4j Data:** Click "Network Devices (Neo4j)"; shows relationships between users, devices, and sensors.
- **Add More Data:** Modify or extend the publisher script to send different payloads and topics.

---

## Key Files and Directories

- `subscriber/` - Python code for MQTT subscriber and publisher, requirements.
- `php/` - PHP scripts and Dockerfile for web dashboard.
- `docker-compose.yml` - Orchestrates all services.
- `README.md` - Original documentation and further details.
- `steps.txt` - Quick commands for setup.

---

## Notes

- Environment variables such as DB passwords, hostnames, and ports are set in scripts; ensure they match your Docker Compose configuration.
- The system is extensible: add more topics or database handlers as needed.
- Designed for learning and experimentation; not hardened for production.

---
