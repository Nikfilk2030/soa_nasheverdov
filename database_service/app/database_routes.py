from flask import jsonify, request
from flask import current_app as app

from database_model import db, User


@app.route('/update', methods=['PUT'])
def update_user():
    # Your update user logic here
    return jsonify({'message': 'User data updated successfully'}), 200
