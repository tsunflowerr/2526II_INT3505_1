from flask import Flask, request, jsonify
import time
import uuid

app = Flask(__name__)

developers = {}

plans = {
    "free": 5,
    "pro": 20
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
        "calls": [],
    }

    return jsonify({
        "api_key": api_key,
        "plan": plan,
        "limit_per_minute": plans[plan]
    })

@app.route("/api/search")
def search():
    api_key = request.headers.get("X-API-Key")

    if api_key not in developers:
        return jsonify({"error": "Invalid API key"}), 401

    developer = developers[api_key]
    now = time.time()

    developer["calls"] = [
        call_time for call_time in developer["calls"]
        if now - call_time < 60
    ]

    limit = plans[developer["plan"]]

    if len(developer["calls"]) >= limit:
        return jsonify({
            "error": "Rate limit exceeded",
            "limit_per_minute": limit
        }), 429

    developer["calls"].append(now)

    q = request.args.get("q", "")

    return jsonify({
        "query": q,
        "result": ["result 1", "result 2"],
        "remaining_calls": limit - len(developer["calls"])
    })

if __name__ == "__main__":
    app.run(debug=True)
