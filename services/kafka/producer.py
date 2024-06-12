import time

from kafka import KafkaProducer

from services.common.constants import KAFKA_SLEEP_TIME


def get_kafka_producer():
    while True:
        try:
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
            return producer
        except Exception:
            time.sleep(KAFKA_SLEEP_TIME)
