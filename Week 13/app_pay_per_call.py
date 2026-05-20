from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

developers = {}
PRICE_PER_CALL = 0.05

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    api_key = str(uuid.uuid4())

    developers[api_key] = {
        "name": data.get("name"),
        "calls": 0
    }

    return jsonify({
        "message": "Registered successfully",
        "api_key": api_key
    })

@app.route("/api/translate")
def translate():
    api_key = request.headers.get("X-API-Key")

    if api_key not in developers:
        return jsonify({"error": "Invalid API key"}), 401

    text = request.args.get("text", "")

    developers[api_key]["calls"] += 1

    return jsonify({
        "original": text,
        "translated": text.upper(),
        "charged": PRICE_PER_CALL
    })

@app.route("/billing")
def billing():
    api_key = request.headers.get("X-API-Key")

    if api_key not in developers:
        return jsonify({"error": "Invalid API key"}), 401

    calls = developers[api_key]["calls"]
    total_cost = round(calls * PRICE_PER_CALL, 2)

    return jsonify({
        "developer": developers[api_key]["name"],
        "total_calls": calls,
        "price_per_call": PRICE_PER_CALL,
        "total_cost": total_cost
    })

if __name__ == "__main__":
    app.run(debug=True)
