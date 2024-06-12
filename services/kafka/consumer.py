import json
import logging
import sqlite3
import time

import kafka

from services.common.constants import KAFKA_SLEEP_TIME
from services.kafka.utils import get_db_name
from services.kafka.utils import get_type
from services.kafka.utils import insert_into_db
from services.kafka.utils import is_duplicate


def create_kafka_consumer():
    while True:
        try:
            consumer = kafka.KafkaConsumer(
                'json_topic',
                bootstrap_servers='kafka:9092',
                auto_offset_reset='earliest',
                group_id='likes_and_views',
                enable_auto_commit=False,
                consumer_timeout_ms=-1
            )
            return consumer
        except Exception as e:
            logging.error(f"Error creating Kafka consumer: {e}")
            time.sleep(KAFKA_SLEEP_TIME)


class KafkaConsumerApp:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        self.logger = logging.getLogger('BEBRA KafkaConsumerApp')
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def consume(self):
        consumer = create_kafka_consumer()
        self.logger.info("Starting to consume messages.")
        try:
            for msg in consumer:
                message = json.loads(msg.value.decode('utf-8'))
                self.logger.info(f"Received message: {message}")

                message_type = get_type(message['type'])
                db_name = get_db_name(message_type)
                self.logger.info(f"DB name on sellected message: {db_name}")

                if is_duplicate(self.cursor, db_name, message):
                    self.logger.info(
                        f"Got duplicate message: Task ID: {message['task_id']}, Username: {message['username']}")
                else:
                    success: bool = insert_into_db(self.cursor, db_name, message)
                    if not success:
                        self.logger.info(
                            f"ERROR wile inserting message: Task ID: {message['task_id']}, Username: {message['username']}")
                    else:
                        self.logger.info(
                            f"Inserted message: Task ID: {message['task_id']}, Username: {message['username']}")
                    self.conn.commit()


                consumer.commit()
        except KeyboardInterrupt:
            self.logger.info("Shutting down consumer due to keyboard interrupt.")
        except Exception as e:
            self.logger.error(f"Error consuming messages: {e}")
        finally:
            consumer.close()
            self.conn.close()
            self.logger.info("Closed database connection and consumer.")
