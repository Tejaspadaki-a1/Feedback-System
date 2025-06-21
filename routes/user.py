from flask import Blueprint, jsonify
from bson import ObjectId
from db import mongo

user_bp = Blueprint('user', __name__)

# ------------------ Get Team Members for a Manager ------------------

@user_bp.route('/team/<manager_id>', methods=['GET'])
def get_team(manager_id):
    try:
        team = mongo.db.users.find({"manager_id": ObjectId(manager_id)})
        result = [
            {
                "_id": str(member["_id"]),
                "name": member["name"],
                "email": member["email"]
            }
            for member in team
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Failed to get team: {str(e)}"}), 500

# ------------------ Get User Profile ------------------

@user_bp.route('/profile/<user_id>', methods=['GET'])
def get_profile(user_id):
    try:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404

        profile = {
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
        return jsonify(profile), 200

    except Exception as e:
        return jsonify({"error": f"Failed to fetch profile: {str(e)}"}), 500
