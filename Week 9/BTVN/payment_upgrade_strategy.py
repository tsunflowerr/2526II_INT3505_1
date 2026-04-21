from flask import Flask, jsonify, request

app = Flask(__name__)


@app.post("/api/v1/payments")
def payment_v1():
    data = request.get_json() or {}
    amount = data.get("amount")

    if not amount:
        return jsonify({"error": "amount is required"}), 400

    return jsonify({
        "version": "v1",
        "message": "payment created",
        "amount": amount,
        "status": "success"
    })


@app.post("/api/v2/payments")
def payment_v2():
    data = request.get_json() or {}
    amount = data.get("amount")
    payment_method = data.get("paymentMethod")
    currency = data.get("currency", "VND")

    if not amount or not payment_method:
        return jsonify({"error": "amount and paymentMethod are required"}), 400

    return jsonify({
        "version": "v2",
        "message": "payment created",
        "payment": {
            "amount": amount,
            "currency": currency,
            "paymentMethod": payment_method,
            "status": "completed"
        }
    })


if __name__ == "__main__":
    app.run(debug=True)
