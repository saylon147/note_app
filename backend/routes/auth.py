from flask import Blueprint, request, jsonify
from extensions import bcrypt, mongo
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user_id = mongo.db.users.insert_one({
        'username': data['username'],
        'password': hashed_password
    }).inserted_id
    return jsonify(message="User registered", user_id=str(user_id)), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({'username': data['username']})
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        access_token = create_access_token(identity=str(user['_id']))
        return jsonify(access_token=access_token)
    return jsonify(message="Invalid credentials"), 401
