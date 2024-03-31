import base64
import grpc
import time

from datetime import datetime

from flask import Flask, request, abort
from flask_restx import Api, Resource, fields

import services.proto.service_pb2_grpc as service_pb2_grpc
import services.proto.service_pb2 as service_pb2
import services.authentication_service.database as database
import services.authentication_service.utils as utils

app = Flask(__name__)
api = Api(app, version='1.0', title='User Service API',
          description='SOA Nasheverdov project')
unique_id_generator = utils.IdGenerator

TASK_CHANNEL = "task_service:51075"


@api.route('/register')
class Register(Resource):
    user_model = api.model('User', {
        'username': fields.String(required=True),
        'password': fields.String(required=True),
        'firstName': fields.String(required=True),
        'lastName': fields.String(required=True),
        'dob': fields.Date(required=True),
        'email': fields.String(required=True),
        'phoneNumber': fields.String(required=True)
    })

    @api.expect(user_model, validate=True)
    def post(self):
        data = request.json
        username = data.get("username")
        password = utils.hash_password(data.get("password"))

        if database.get_user(username):
            return {'message': 'User already exists'}, 400

        database.create_user(
            username=username,
            password=password,
            firstName=data.get("firstName"),
            lastName=data.get("lastName"),
            dob=data.get("dob"),
            email=data.get("email"),
            phoneNumber=data.get("phoneNumber")
        )

        return {'message': 'User successfully registered'}, 201


@api.route('/auth')
class Auth(Resource):
    auth_model = api.model('Auth', {
        'username': fields.String(required=True),
        'password': fields.String(required=True)
    })

    @api.expect(auth_model, validate=True)
    def post(self):
        data = request.json
        username = data.get('username')
        password = utils.hash_password(data.get('password'))

        # return {'message': f'{username} {password}'}

        if utils.verify_user(database, username, password):
            return {'message': 'User successfully authenticated'}, 200
        else:
            return {'message': 'Unauthorized, check login credentials'}, 401


@api.route('/update_user')
class UpdateUser(Resource):
    update_model = api.model('UpdateUser', {
        'firstName': fields.String(required=True),
        'lastName': fields.String(required=True),
        'dob': fields.Date(required=True),
        'email': fields.String(required=True),
        'phoneNumber': fields.String(required=True)
    })

    @api.expect(update_model, validate=True)
    def put(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            return {'message': 'Unauthorized, check login credentials'}, 401

        base64_creds = auth_header.split(' ')[1]
        creds = base64.b64decode(base64_creds).decode('utf-8')
        username, password = creds.split(':')
        password = utils.hash_password(password)

        if not utils.verify_user(database, username, password):
            return {'message': 'Unauthorized, check login credentials'}, 401

        data = request.json
        database.update_user(
            username=username,
            firstName=data.get("firstName"),
            lastName=data.get("lastName"),
            dob=data.get("dob"),
            email=data.get("email"),
            phoneNumber=data.get("phoneNumber")
        )

        return {'message': 'User data updated successfully'}, 200


@api.route('/create_task')
class Auth(Resource):
    create_task_model = api.model('CreateTask', {
        'username': fields.String(required=True),
        'password': fields.String(required=True),
        'content': fields.String(required=True),
    })

    @api.expect(create_task_model, validate=True)
    def post(self):
        unix_timestamp = time.time()
        current_time = datetime.utcfromtimestamp(unix_timestamp)
        iso_current_time = current_time.isoformat() + "Z"

        data = request.json
        username = data.get('username')
        password = utils.hash_password(data.get('password'))

        if not utils.verify_user(database, username, password):
            return {'message': 'Unauthorized, check login credentials'}, 401

        with grpc.insecure_channel(TASK_CHANNEL) as channel:
            stub = service_pb2_grpc.TaskServiceStub(channel)
            unique_id = unique_id_generator.get_next_id
            task = service_pb2.Task(
                id=str(unique_id),
                username=username,
                content=data.get('content'),
                date=iso_current_time,
                tag=data.get('tag')
            )
            task_response = stub.CreateTask(task)

        if task_response.status == 0:
            return {'message': 'Error while creating task'}, 401

        return {
            'message': f'Successfully created task with status {task_response.status}, task_id {task_response.task.id}'}, 200


# @app.route('/create_task', methods=['POST'])
# def create_task():
#     create_task_model = api.model('CreateTask', {
#         'username': fields.String(required=True),
#         'password': fields.String(required=True)
#     })
#     # Authentication logic to retrieve user_id
#     data = request.json
#     try:
#         task = service_pb2.Task(title=content['title'], description=content['description'], user_id="user_id_example")
#         response = service_pb2_grpc.CreateTask(task)
#         return jsonify(task=response.task), 201
#     except Exception as e:
#         abort(500, description=str(e))


if __name__ == 'main':
    app.run(debug=True)
