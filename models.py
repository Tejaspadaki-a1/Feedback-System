from bson import ObjectId
from db import mongo

# --------- User Functions ---------
def find_user_by_email(email):
    return mongo.db.users.find_one({"email": email})

def find_user_by_id(user_id):
    return mongo.db.users.find_one({"_id": ObjectId(user_id)})

def insert_user(user_data):
    return mongo.db.users.insert_one(user_data)

def update_user(user_id, updates):
    return mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": updates})

def get_all_managers():
    managers = mongo.db.users.find({"role": "manager"})
    return [{"_id": str(m["_id"]), "name": m["name"]} for m in managers]

# --------- Feedback Functions ---------
def insert_feedback(feedback_data):
    return mongo.db.feedbacks.insert_one(feedback_data)

def get_feedbacks_by_employee(employee_id):
    return list(mongo.db.feedbacks.find({"employee_id": ObjectId(employee_id)}))

def get_feedbacks_by_manager(manager_id):
    return list(mongo.db.feedbacks.find({"manager_id": ObjectId(manager_id)}))

def update_feedback(feedback_id, data):
    return mongo.db.feedbacks.update_one(
        {"_id": ObjectId(feedback_id)},
        {"$set": data}
    )
