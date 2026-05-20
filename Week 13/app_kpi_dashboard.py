from flask import Flask, request, jsonify
import uuid
import random

app = Flask(__name__)

developers = {}
stats = {
    "call_volume": 0,
    "error_count": 0
}

@app.route("/")
def dashboard():
    total_calls = stats["call_volume"]
    error_rate = 0

    if total_calls > 0:
        error_rate = round(stats["error_count"] / total_calls * 100, 2)

    return f"""
    <h1>API Product KPI Dashboard</h1>

    <ul>
        <li>Registered Developers: {len(developers)}</li>
        <li>Call Volume: {stats["call_volume"]}</li>
        <li>Error Count: {stats["error_count"]}</li>
        <li>Error Rate: {error_rate}%</li>
    </ul>
    """

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    api_key = str(uuid.uuid4())

    developers[api_key] = {
        "name": data.get("name"),
        "email": data.get("email")
    }

    return jsonify({
        "message": "Registered successfully",
        "api_key": api_key
    })

@app.route("/api/data")
def data():
    stats["call_volume"] += 1

    if random.random() < 0.2:
        stats["error_count"] += 1
        return jsonify({"error": "API error"}), 500

    return jsonify({
        "message": "Successful API response"
    })

if __name__ == "__main__":
    app.run(debug=True)
