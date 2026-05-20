from flask import Flask, jsonify, request
import random

app = Flask(__name__)

analytics = {
    "total_calls": 0,
    "success_calls": 0,
    "error_calls": 0
}

@app.before_request
def count_call():
    if request.path.startswith("/api/"):
        analytics["total_calls"] += 1

@app.route("/")
def home():
    return """
    <h1>API Analytics Demo</h1>
    <p>GET /api/product/1</p>
    <p>GET /api/analytics</p>
    """

@app.route("/api/product/<int:product_id>")
def get_product(product_id):
    if random.random() < 0.25:
        analytics["error_calls"] += 1
        return jsonify({"error": "Random server error"}), 500

    analytics["success_calls"] += 1
    return jsonify({
        "id": product_id,
        "name": "Demo Product",
        "price": 99
    })

@app.route("/api/analytics")
def get_analytics():
    total = analytics["total_calls"]
    error = analytics["error_calls"]

    error_rate = 0
    if total > 0:
        error_rate = round(error / total * 100, 2)

    return jsonify({
        "total_calls": total,
        "success_calls": analytics["success_calls"],
        "error_calls": error,
        "error_rate_percent": error_rate
    })

if __name__ == "__main__":
    app.run(debug=True)
