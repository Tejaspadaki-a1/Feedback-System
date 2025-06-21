from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from bson import ObjectId
from models import (
    find_user_by_email,
    insert_user,
    update_user,
    get_all_managers
)

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = 'supersecretkey'  # Move to env in production

# ------------------------ Register ------------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({"error": "Missing required fields"}), 400

    if find_user_by_email(data['email']):
        return jsonify({"error": "User already exists"}), 409

    hashed_pw = generate_password_hash(data['password'])

    user = {
        "name": data['name'],
        "email": data['email'],
        "password_hash": hashed_pw,
        "role": data['role'],
        "manager_id": None
    }

    result = insert_user(user)
    inserted_id = result.inserted_id

    if data['role'] == 'manager':
        update_user(inserted_id, {"manager_id": inserted_id})
    elif data.get('manager_id'):
        update_user(inserted_id, {"manager_id": ObjectId(data['manager_id'])})

    return jsonify({"msg": "User registered"}), 201

# ------------------------ Login ------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = find_user_by_email(data['email'])

    if user and check_password_hash(user['password_hash'], data['password']):
        payload = {
            "user_id": str(user['_id']),
            "role": user['role'],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({"token": token})

    return jsonify({"error": "Invalid credentials"}), 401

# ------------------------ Managers List ------------------------
@auth_bp.route('/managers', methods=['GET'])
def get_managers():
    return jsonify(get_all_managers())
