import paho.mqtt.publish as publish
import time
import random
import json

BROKER = "localhost"

users = ["alice", "bob", "carol"]
devices = ["dev001", "dev002", "dev003"]
sensors = ["temp", "humidity", "motion"]

def random_device_status():
    return random.choice(["online", "offline", "idle"])

def generate_mysql_data():
    temp = round(random.uniform(20, 30), 2)
    return ("temperature/room1", f"{temp}")

def generate_mongo_data():
    sensor_data = {
        "humidity": random.randint(30, 70),
        "pressure": random.randint(950, 1050)
    }
    return ("sensor/" + random.choice(devices), json.dumps(sensor_data))

def generate_neo4j_data():
    data = {
        "user": random.choice(users),
        "device": random.choice(devices),
        "sensor": random.choice(sensors),
        "reading": round(random.uniform(10, 100), 2),
        "status": random_device_status(),
        "timestamp": time.time()
    }
    return ("graph/iot", json.dumps(data))

while True:
    for generator in [generate_mysql_data, generate_mongo_data, generate_neo4j_data]:
        topic, msg = generator()
        print(f"Publishing to {topic}: {msg}")
        publish.single(topic, msg, hostname=BROKER)
        time.sleep(1)
