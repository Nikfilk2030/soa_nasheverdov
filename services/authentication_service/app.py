import base64
import json
import time
from datetime import datetime

import grpc
from flask import Flask
from flask import request
from flask_restx import Api
from flask_restx import fields
from flask_restx import Resource
from google.protobuf.json_format import MessageToDict

import services.authentication_service.database as database
import services.authentication_service.utils as utils
import services.proto.service_pb2 as service_pb2
import services.proto.service_pb2_grpc as service_pb2_grpc

from services.kafka.producer import get_kafka_producer

app = Flask(__name__)
api = Api(app, version='1.0', title='User Service API',
          description='SOA Nasheverdov project')
CURRENT_TASK_ID = 0

TASK_CHANNEL = "task_service:51075"


class EStatus:
    ERROR = 228
    SUCCESS = 1337


KAFKA_PRODUCER = get_kafka_producer()


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
class CreateTask(Resource):
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

            global CURRENT_TASK_ID
            CURRENT_TASK_ID += 1

            task = service_pb2.Task(
                id=CURRENT_TASK_ID,
                username=username,
                content=data.get('content'),
                date=iso_current_time,
                tag='0'  # TODO implement tag logic, now it is unnecessary
            )
            task_response = stub.CreateTask(task)

        if task_response.status == EStatus.ERROR:
            return {'message': 'Error while creating task'}, 401

        return {
            'message': f'Successfully created task with status {task_response.status}, task_id {task_response.task.id}'}, 200


@api.route('/update_task')
class UpdateTask(Resource):
    update_task_model = api.model('UpdateTask', {
        'username': fields.String(required=True),
        'password': fields.String(required=True),
        'task_id': fields.Integer(required=True),
        'content': fields.String(required=True),
    })

    @api.expect(update_task_model, validate=True)
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
            task = service_pb2.Task(
                id=data.get('task_id'),
                username=username,
                content=data.get('content'),
                date=iso_current_time,
                tag='0'  # TODO implement tag logic, now it is unnecessary
            )
            task_response = stub.UpdateTask(task)

        if task_response.status == EStatus.ERROR:
            return {'message': 'Error while updating task'}, 401

        return {
            'message': f'Successfully updated task with status {task_response.status}, task_id {task_response.task.id}'}, 200


@api.route('/delete_task')
class UpdateTask(Resource):
    delete_task_model = api.model('DeleteTask', {
        'username': fields.String(required=True),
        'password': fields.String(required=True),
        'task_id': fields.Integer(required=True)
    })

    @api.expect(delete_task_model, validate=True)
    def post(self):
        data = request.json
        username = data.get('username')
        password = utils.hash_password(data.get('password'))

        if not utils.verify_user(database, username, password):
            return {'message': 'Unauthorized, check login credentials'}, 401

        with grpc.insecure_channel(TASK_CHANNEL) as channel:
            stub = service_pb2_grpc.TaskServiceStub(channel)
            task_id = service_pb2.TaskID(
                id=data.get('task_id'),
            )
            delete_response = stub.DeleteTask(task_id)

        if not delete_response.success:
            return {'message': 'Error while deleting task'}, 401

        return {
            'message': f'Successfully deleted task with status {delete_response.success}'}, 200


@api.route('/get_task_by_id')
class GetTaskByID(Resource):
    get_task_model = api.model('GetTask', {
        'username': fields.String(required=True),
        'password': fields.String(required=True),
        'task_id': fields.Integer(required=True)
    })

    @api.expect(get_task_model, validate=True)
    def get(self):
        data = request.json
        username = data.get('username')
        password = utils.hash_password(data.get('password'))

        if not utils.verify_user(database, username, password):
            return {'message': 'Unauthorized, check login credentials'}, 401

        with grpc.insecure_channel(TASK_CHANNEL) as channel:
            stub = service_pb2_grpc.TaskServiceStub(channel)
            task_id = service_pb2.TaskID(id=data.get('task_id'))
            task_response = stub.GetTaskByID(task_id)

        if task_response.status != EStatus.SUCCESS:
            return {'message': 'Task not found or error encountered'}, 404

        task_data = MessageToDict(task_response.task)
        return {
            'message': 'Task retrieved successfully',
            'task': task_data
        }, 200


@api.route('/get_tasks')
class GetTasks(Resource):
    get_tasks_model = api.model('GetTasks', {
        'username': fields.String(required=True),
        'password': fields.String(required=True),
        'page_number': fields.String(required=True),
        'page_size': fields.String(required=True),
    })

    @api.expect(get_tasks_model, validate=True)
    def get(self):
        data = request.json
        username = data.get('username')
        password = utils.hash_password(data.get('password'))

        if not utils.verify_user(database, username, password):
            return {'message': 'Unauthorized, check login credentials'}, 401

        with grpc.insecure_channel(TASK_CHANNEL) as channel:
            stub = service_pb2_grpc.TaskServiceStub(channel)
            params = service_pb2.PaginationParams(
                page_number=data.get('page_number'),
                page_size=data.get('page_size')
            )
            response = stub.GetTasks(params)

        if response.status != EStatus.SUCCESS:
            return {'message': 'Tasks not found or error encountered'}, 404

        id_to_task = {}
        for task in response.tasks:
            task_data = MessageToDict(task)
            id_to_task[task.id] = task_data
        return {
            'message': 'Tasks retrieved successfully',
            'tasks': id_to_task
        }, 200


@api.route('/send_like')
class SendLike(Resource):
    send_like_model = api.model('GetTasks', {
        'username': fields.String(required=True),
        'password': fields.String(required=True),
        'task_id': fields.Integer(required=True),
    })

    @api.expect(send_like_model, validate=True)
    def post(self):
        data = request.json
        username = data.get('username')
        password = utils.hash_password(data.get('password'))

        if not utils.verify_user(database, username, password):
            return {'message': 'Unauthorized, check login credentials'}, 401

        # TODO validation that task_id exist?

        data['type'] = 'like'

        KAFKA_PRODUCER.send('json_topic', json.dumps(data).encode('utf-8'))

        return {
            'message': 'Like succesfully sent to Kafka'
        }, 200


@api.route('/send_view')
class GetTasks(Resource):
    send_view_model = api.model('GetTasks', {
        'username': fields.String(required=True),
        'password': fields.String(required=True),
        'task_id': fields.Integer(required=True),
    })

    @api.expect(send_view_model, validate=True)
    def post(self):
        data = request.json
        username = data.get('username')
        password = utils.hash_password(data.get('password'))

        if not utils.verify_user(database, username, password):
            return {'message': 'Unauthorized, check login credentials'}, 401

        # TODO validation that task_id exist?

        data['type'] = 'view'

        KAFKA_PRODUCER.send('json_topic', json.dumps(data).encode('utf-8'))

        return {
            'message': 'View succesfully sent to Kafka'
        }, 200


if __name__ == '__main__':
    app.run(debug=True)
