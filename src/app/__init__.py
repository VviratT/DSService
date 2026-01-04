print("🟢 app/__init__.py START")

from flask import Flask
print("🟢 Flask imported")

app = Flask(__name__)
print("🟢 Flask app created")

app.config.from_pyfile('config.py')
print("🟢 config loaded")

from app.service.messageService import MessageService
print("🟢 MessageService imported")

print("🟢 app/__init__.py END")


from flask import request, jsonify
from app import app
import json

messageService = MessageService()

def get_producer():
    from kafka import KafkaProducer   # ✅ LAZY IMPORT (CRITICAL)
    return KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        api_version=(2, 5, 0),
        request_timeout_ms=5000,
        api_version_auto_timeout_ms=5000
    )

@app.route("/", methods=["GET"])
def health_check():
    return "Expense Service is running!"

@app.route("/v1/ds/message", methods=["POST"])
def handle_message():
    data = request.get_json()
    message = data.get("message")

    result = messageService.process_message(message)

    producer = get_producer()
    producer.send("expense_service", result.dict())
    producer.flush()

    return jsonify(result.dict())
