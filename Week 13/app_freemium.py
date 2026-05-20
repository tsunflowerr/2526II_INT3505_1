from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

developers = {}

plans = {
    "free": {
        "limit": 3,
        "price": 0
    },
    "pro": {
        "limit": 10,
        "price": 20
    }
}

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    plan = data.get("plan", "free")

    if plan not in plans:
        return jsonify({"error": "Invalid plan"}), 400

    api_key = str(uuid.uuid4())

    developers[api_key] = {
        "name": data.get("name"),
        "plan": plan,
        "usage": 0
    }

    return jsonify({
        "message": "Registered successfully",
        "api_key": api_key,
        "plan": plan,
        "limit": plans[plan]["limit"]
    })

@app.route("/api/premium-data")
def premium_data():
    api_key = request.headers.get("X-API-Key")

    if api_key not in developers:
        return jsonify({"error": "Invalid API key"}), 401

    developer = developers[api_key]
    plan = developer["plan"]
    limit = plans[plan]["limit"]

    if developer["usage"] >= limit:
        return jsonify({
            "error": "API limit reached",
            "plan": plan,
            "upgrade_message": "Upgrade to pro for more requests"
        }), 429

    developer["usage"] += 1

    return jsonify({
        "data": "This is premium API data",
        "plan": plan,
        "usage": developer["usage"],
        "limit": limit
    })

if __name__ == "__main__":
    app.run(debug=True)
