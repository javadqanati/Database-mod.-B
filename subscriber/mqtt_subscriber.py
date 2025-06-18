import paho.mqtt.client as mqtt
import pymongo
import mysql.connector
from py2neo import Graph, Node, Relationship
import logging
import json

MQTT_BROKER = "host.docker.internal"
MQTT_PORT = 1883

MYSQL_CONFIG = {
    "host": "mysql",
    "port": 3306,
    "user": "root",
    "password": "1234test",
    "database": "iot_data"
}

MONGO_URI = "mongodb://mongodb:27017/"
NEO4J_URI = "bolt://neo4j:7687"
NEO4J_AUTH = ("neo4j", "test1234")

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

class MySQLHandler:
    def __init__(self, config):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS temperature_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                topic VARCHAR(255),
                value TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def insert(self, topic, value):
        try:
            self.cursor.execute("INSERT INTO temperature_data (topic, value) VALUES (%s, %s)", (topic, value))
            self.conn.commit()
            logging.info(f"✅ Stored in MySQL: {topic} → {value}")
        except Exception as e:
            logging.error(f"MySQL error: {e}")


class MongoHandler:
    def __init__(self, uri):
        self.client = pymongo.MongoClient(uri)
        self.collection = self.client["iot_data"]["sensor_data"]

    def insert(self, topic, value):
        try:
            logging.info(f"Attempting MongoDB insert: {topic} → {value}")
            self.collection.insert_one({
                "topic": topic,
                "value": value
            })
            logging.info(f"Stored in MongoDB: {topic}")
        except Exception as e:
            logging.error(f"MongoDB insert failed: {e}")


class Neo4jHandler:
    def __init__(self, uri):
        self.graph = Graph(uri, auth=NEO4J_AUTH)

    def store_iot_data(self, payload):
        try:
            user_name = payload.get("user", "unknown_user")
            device_name = payload.get("device", "unknown_device")
            sensor_type = payload.get("sensor", "unknown_sensor")
            reading = payload.get("reading")
            status = payload.get("status")
            timestamp = payload.get("timestamp")

            user_node = Node("User", name=user_name)
            device_node = Node("Device", name=device_name)
            sensor_node = Node("Sensor", type=sensor_type)

            self.graph.merge(user_node, "User", "name")
            self.graph.merge(device_node, "Device", "name")
            self.graph.merge(sensor_node, "Sensor", "type")

            owns_rel = Relationship(user_node, "OWNS", device_node)
            reports_rel = Relationship(device_node, "REPORTS", sensor_node,
                                       reading=reading, status=status, timestamp=timestamp)

            self.graph.merge(owns_rel)
            self.graph.create(reports_rel)

            logging.info(f"Stored in Neo4j: {user_name} → {device_name} → {sensor_type}")

        except Exception as e:
            logging.error(f"Neo4j error: {e}")

class MQTTSubscriber:
    def __init__(self):
        self.mysql = MySQLHandler(MYSQL_CONFIG)
        self.mongo = MongoHandler(MONGO_URI)
        self.neo4j = Neo4jHandler(NEO4J_URI)

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, reason_code, properties=None):
        logging.info(f"Connected to MQTT broker with result code: {reason_code}")
        result, mid = client.subscribe("#")
        logging.info(f"Subscription result: {result}, message ID: {mid}")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        topic = msg.topic
        logging.info(f"Received: {topic} → {payload}")

        if topic.startswith("temperature/"):
            self.mysql.insert(topic, payload)

        elif topic.startswith("sensor/"):
            self.mongo.insert(topic, payload)

        elif topic.startswith("graph/"):
            try:
                data = json.loads(payload)
                self.neo4j.store_iot_data(data)
            except Exception as e:
                logging.error(f"Failed to store graph data in Neo4j: {e}")

    def run(self):
        logging.info("Connecting to MQTT broker...")
        self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        logging.info("Starting MQTT loop...")
        self.client.loop_forever()


if __name__ == "__main__":
    MQTTSubscriber().run()
