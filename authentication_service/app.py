from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

app = Flask(__name__)

# Dummy database for the example
users = {}


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    # ... Other fields

    if username in users:
        return make_response('User already exists', 400)

    hashed_password = generate_password_hash(password)
    users[username] = {
        'id': uuid.uuid4(),
        'password': hashed_password,
        # ... Other fields
    }
    return make_response('User successfully registered', 201)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username not in users or not check_password_hash(users[username]['password'], password):
        return make_response('Unauthorized, check login credentials', 401)

    return make_response('User successfully authenticated', 200)


if __name__ == 'main':
    app.run(debug=True)