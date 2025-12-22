import os
from pymongo import MongoClient
from datetime import datetime


# MongoDB connection (env var)
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["userdb"]
users = db["users"]

def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": "Method Not Allowed"
        }

    data = request.json

    doc = {
        "username": data.get("username"),
        "password": data.get("password"),
        "ip": request.headers.get("x-forwarded-for"),
        "user_agent": request.headers.get("user-agent"),
        "timestamp": datetime.utcnow()
        
    }

    users.insert_one(doc)

    return {
        "statusCode": 201,
        "body": "Stored"
    }

