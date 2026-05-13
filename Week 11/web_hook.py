# demos/webhook.py
from flask import Blueprint, jsonify, request
import requests

webhook_bp = Blueprint("webhook", __name__, url_prefix="/webhooks")

registered_webhooks = []


@webhook_bp.post("/register")
def register_webhook():
    data = request.get_json()

    url = data["url"]

    registered_webhooks.append(url)

    return jsonify({
        "message": "Webhook registered",
        "url": url
    }), 201


@webhook_bp.get("/registered")
def get_registered_webhooks():
    return jsonify(registered_webhooks)


@webhook_bp.post("/payment")
def payment_success():
    data = request.get_json()

    payment_event = {
        "event": "PAYMENT_SUCCESS",
        "payment_id": data["payment_id"],
        "amount": data["amount"]
    }

    results = []

    for url in registered_webhooks:
        try:
            response = requests.post(url, json=payment_event, timeout=3)

            results.append({
                "url": url,
                "status_code": response.status_code
            })
        except requests.RequestException as error:
            results.append({
                "url": url,
                "error": str(error)
            })

    return jsonify({
        "message": "Payment event sent to webhooks",
        "event": payment_event,
        "webhook_results": results
    })


@webhook_bp.post("/client-receiver")
def client_receiver():
    data = request.get_json()

    return jsonify({
        "message": "Client received webhook",
        "received_data": data
    })