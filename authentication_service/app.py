import base64
import hashlib

from flask import Flask, request
from flask_restx import Api, Resource, fields

from database import get_user, create_user, update_user

app = Flask(__name__)
api = Api(app, version='1.0', title='User Service API',
          description='SOA Nasheverdov project')

user_model = api.model('User', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'firstName': fields.String(required=True),
    'lastName': fields.String(required=True),
    'dob': fields.Date(required=True),
    'email': fields.String(required=True),
    'phoneNumber': fields.String(required=True)
})

auth_model = api.model('Auth', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

update_model = api.model('UpdateUser', {
    'firstName': fields.String(required=True),
    'lastName': fields.String(required=True),
    'dob': fields.Date(required=True),
    'email': fields.String(required=True),
    'phoneNumber': fields.String(required=True)
})


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(input_password: str, stored_hashed_password: str) -> bool:
    return hashlib.md5(input_password.encode()).hexdigest() == stored_hashed_password


def verify_user(username: str, password: str) -> bool:
    user = get_user(username)

    return user and verify_password(input_password=user[2], stored_hashed_password=password)


@api.route('/register')
class Register(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        data = request.json
        username = data.get("username")
        password = hash_password(data.get("password"))

        if get_user(username):
            return {'message': 'User already exists'}, 400

        create_user(
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
    @api.expect(auth_model, validate=True)
    def post(self):
        data = request.json
        username = data.get('username')
        password = hash_password(data.get('password'))

        if verify_user(username, password):
            return {'message': 'User successfully authenticated'}, 200
        else:
            return {'message': 'Unauthorized, check login credentials'}, 401


@api.route('/update')
class UpdateUser(Resource):
    @api.expect(update_model, validate=True)
    def put(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            return {'message': 'Unauthorized, check login credentials'}, 401

        base64_creds = auth_header.split(' ')[1]
        creds = base64.b64decode(base64_creds).decode('utf-8')
        username, password = creds.split(':')
        password = hash_password(password)

        if not verify_user(username, password):
            return {'message': 'Unauthorized, check login credentials'}, 401

        data = request.json
        update_user(
            username=username,
            firstName=data.get("firstName"),
            lastName=data.get("lastName"),
            dob=data.get("dob"),
            email=data.get("email"),
            phoneNumber=data.get("phoneNumber")
        )

        return {'message': 'User data updated successfully'}, 200


if __name__ == 'main':
    app.run(debug=True)
