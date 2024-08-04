from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, unset_jwt_cookies
)
from utils.models import User
from utils.extensions import bcrypt
from datetime import datetime

auth = Blueprint('auth', __name__)


ERROR_CODES = {
    400: "Bad Request",
    401: "Unauthorized",
    404: "Not Found",
    500: "Internal Server Error",
}


def create_response(message, status_code):
    return (jsonify({"msg": message, "status": status_code,
                    "error": ERROR_CODES.get(status_code, "")}),
            status_code)


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.objects(username=username).first():
        return create_response("Username already exists", 400)

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, password=hashed_password)
    user.save()

    return create_response("User registered successfully", 200)


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.objects(username=username).first()
    if not user:
        return create_response("User not found", 404)

    if not user.verify_password(password):
        return create_response("Password does not match", 401)

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@auth.route('/resetpwd', methods=['POST'])
def resetpwd():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.objects(username=username).first()
    if not user:
        return create_response("User not found", 404)

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user.password = hashed_password
    user.save()

    return create_response("Password reset successfully", 200)
