import threading

import flask
from flask import Flask
from flask_restx import Api
from flask_restx import Resource

from services.statistics_service.database import run_kafka


class KafkaDB:
    def __init__(self):
        kafka_consumer_thread = threading.Thread(target=run_kafka)
        kafka_consumer_thread.start()


# app = Flask(__name__)
# api = Api(app, version='1.0', title='Statistics service',
#           description='Kafka')
#
#
# @api.route('/alive')
# class GetAlive(Resource):
#     def get(self):
#         return {
#             'message': 'Alive'
#         }, 200
#
#
# if __name__ == '__main__':
#     app.run(debug=True)


def create_app() -> Flask:
    app = Flask(__name__)
    db = KafkaDB()

    @app.route('/alive', methods=['GET'])
    def alive():
        response = flask.make_response()
        response.status_code = 200
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=51076)
