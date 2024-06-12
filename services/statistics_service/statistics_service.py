import sqlite3
import threading
import flask
from flask import Flask, make_response

import services.kafka.consumer as kafka_consumer  # TODO remove?

DATABASE = '/data/users.db'  # TODO пока хардкодим, потом унести


def get_connection():
    return sqlite3.connect(DATABASE)


def run_cafka_and_create_db():
    import services.kafka.consumer as kafka_consumer

    conn = get_connection()

    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS stats_data;")
    cursor.execute('''
                    CREATE TABLE stats_data (
                        task_id INTEGER PRIMARY KEY, 
                        username TEXT
                    );
                ''')

    conn.commit()

    consumer = kafka_consumer.KafkaConsumerApp(DATABASE)
    consumer.consume()


class PostgressStatsDB():
    def __init__(self):
        kafka_consumer_thread = threading.Thread(target=run_cafka_and_create_db)
        kafka_consumer_thread.start()


def create_app() -> Flask:
    app = Flask(__name__)
    stats = PostgressStatsDB()

    @app.route('/alive', methods=['GET'])
    def alive():
        response = flask.make_response()
        response.status_code = 200
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=51076)
