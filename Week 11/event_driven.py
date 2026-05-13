# demos/event_driven.py
from flask import Blueprint, jsonify, request
from queue import Queue
from threading import Thread
import time

event_bp = Blueprint("events", __name__, url_prefix="/events")

event_queue = Queue()
event_logs = []


def event_worker():
    while True:
        event = event_queue.get()

        time.sleep(1)

        log = {
            "event": event["type"],
            "payload": event["payload"],
            "status": "processed"
        }

        event_logs.append(log)
        event_queue.task_done()


worker = Thread(target=event_worker, daemon=True)
worker.start()


@event_bp.post("/orders")
def create_order():
    data = request.get_json()

    order = {
        "id": int(time.time()),
        "product": data["product"],
        "quantity": data["quantity"]
    }

    event_queue.put({
        "type": "ORDER_CREATED",
        "payload": order
    })

    return jsonify({
        "message": "Order received",
        "order": order,
        "note": "Order will be processed asynchronously"
    }), 202


@event_bp.get("/logs")
def get_event_logs():
    return jsonify(event_logs)