from flask import Blueprint, request, jsonify
from bson import ObjectId
from db import mongo
import datetime

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['POST'])
def create_feedback():
    data = request.get_json()
    feedback = {
        "manager_id": ObjectId(data['manager_id']),
        "employee_id": ObjectId(data['employee_id']),
        "strengths": data['strengths'],
        "improvements": data['improvements'],
        "sentiment": data['sentiment'],
        "tags": data.get('tags', []),
        "acknowledged": False,
        "employee_comment": "",
        "anonymous": data.get('anonymous', False),
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow()
    }
    mongo.db.feedbacks.insert_one(feedback)
    return jsonify({"msg": "Feedback created"}), 201

@feedback_bp.route('/feedback/self/<employee_id>', methods=['GET'])
def get_employee_feedback(employee_id):
    feedbacks = mongo.db.feedbacks.find({"employee_id": ObjectId(employee_id)})
    return jsonify([
        {
            "_id": str(f["_id"]),
            "manager_id": str(f["manager_id"]),
            "employee_id": str(f["employee_id"]),
            "strengths": f["strengths"],
            "improvements": f["improvements"],
            "sentiment": f["sentiment"],
            "tags": f.get("tags", []),
            "acknowledged": f.get("acknowledged", False),
            "employee_comment": f.get("employee_comment", ""),
            "anonymous": f.get("anonymous", False),
            "created_at": f["created_at"].isoformat(),
            "updated_at": f["updated_at"].isoformat()
        } for f in feedbacks
    ])

@feedback_bp.route('/feedback/manager/<manager_id>', methods=['GET'])
def get_manager_feedbacks(manager_id):
    feedbacks = mongo.db.feedbacks.find({"manager_id": ObjectId(manager_id)})
    return jsonify([
        {
            "_id": str(f["_id"]),
            "manager_id": str(f["manager_id"]),
            "employee_id": str(f["employee_id"]),
            "strengths": f["strengths"],
            "improvements": f["improvements"],
            "sentiment": f["sentiment"],
            "tags": f.get("tags", []),
            "acknowledged": f.get("acknowledged", False),
            "employee_comment": f.get("employee_comment", ""),
            "anonymous": f.get("anonymous", False),
            "created_at": f["created_at"].isoformat(),
            "updated_at": f["updated_at"].isoformat()
        } for f in feedbacks
    ])

@feedback_bp.route('/feedback/<feedback_id>/acknowledge', methods=['POST'])
def acknowledge_feedback(feedback_id):
    mongo.db.feedbacks.update_one(
        {"_id": ObjectId(feedback_id)},
        {"$set": {"acknowledged": True, "updated_at": datetime.datetime.utcnow()}}
    )
    return jsonify({"msg": "Acknowledged"})

@feedback_bp.route('/feedback/<feedback_id>/comment', methods=['POST'])
def comment_on_feedback(feedback_id):
    comment = request.json.get("comment")
    mongo.db.feedbacks.update_one(
        {"_id": ObjectId(feedback_id)},
        {"$set": {"employee_comment": comment, "updated_at": datetime.datetime.utcnow()}}
    )
    return jsonify({"msg": "Comment added"})
