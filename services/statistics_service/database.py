import sqlite3

import services.kafka.consumer as kafka_consumer

DATABASE = '/data/stats_data.db'


def get_connection(database):
    return sqlite3.connect(database)


def create_likes(cursor):
    cursor.execute("DROP TABLE IF EXISTS likes;")
    cursor.execute('''
        CREATE TABLE likes (
            task_id INTEGER PRIMARY KEY, 
            username TEXT
        );
    ''')


def create_views(cursor):
    cursor.execute("DROP TABLE IF EXISTS views;")
    cursor.execute('''
        CREATE TABLE views (
            task_id INTEGER PRIMARY KEY,
            username TEXT
        );
    ''')


def run_kafka():
    conn = get_connection(DATABASE)

    cursor = conn.cursor()
    create_likes(cursor)
    create_views(cursor)
    conn.commit()

    consumer = kafka_consumer.KafkaConsumerApp(DATABASE)
    consumer.consume()
