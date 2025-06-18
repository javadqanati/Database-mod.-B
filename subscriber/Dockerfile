FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY mqtt_subscriber.py .
COPY wait-for-it.sh .

CMD ["./wait-for-it.sh", "neo4j", "7687", "python", "mqtt_subscriber.py"]
