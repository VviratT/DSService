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
import os
# import jsonpickle

messageService = MessageService()

def get_producer():
    from kafka import KafkaProducer   # ✅ LAZY IMPORT (CRITICAL)
    kafka_host = os.getenv('KAFKA_HOST', 'localhost')
    kafka_port = os.getenv('KAFKA_PORT', '9092')
    kafka_bootstrap_servers = f"{kafka_host}:{kafka_port}"
    return KafkaProducer(
        bootstrap_servers=kafka_bootstrap_servers,
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
    user_id = request.headers.get('x-user-id')
    if not user_id:
        return jsonify({'error': 'x-user-id header is required'}), 400

    data = request.get_json()
    message = data.get("message")

    result = messageService.process_message(message)

    producer = get_producer()
    if result is not None:
        serialized_result = result.serialize()
        serialized_result['user_id'] = user_id
        producer.send('expense_service', serialized_result)
        producer.flush()
        return jsonify(serialized_result)
    else:
        return jsonify({'error': 'Invalid message format'}), 400


