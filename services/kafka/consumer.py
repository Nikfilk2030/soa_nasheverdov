import json
import logging
import sqlite3
import time

import kafka


KAFKA_SLEEP_TIME = 5  # seconds


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


class EType:
    Like = 1
    View = 2


def get_type(t: str) -> int:
    if t == 'like':
        return EType.Like
    if t == 'view':
        return EType.View
    raise Exception('unknown EType in get_type')


def is_like(t: int) -> bool:
    return t == EType.Like


def is_view(t: int) -> bool:
    return t == EType.View


def get_db_name(t: int) -> str:
    if is_like(t):
        return 'likes'
    if is_view(t):
        return 'views'
    raise Exception('unknown EType in get_db_name')


class KafkaConsumerApp:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

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

                self.cur.execute(f"SELECT 1 FROM {db_name} WHERE task_id = ? AND username = ?",
                                 (message['task_id'], message['username']))
                result = self.cur.fetchone()
                if not result:
                    self.cur.execute(
                        f"INSERT INTO {db_name} (task_id, username) VALUES (?, ?)",
                        (message['task_id'], message['username']))
                    if self.cur.rowcount == 0:
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
