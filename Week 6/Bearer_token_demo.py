from flask import Flask, request, jsonify

app = Flask(__name__)

VALID_TOKEN = "demo-secret-token"


@app.route("/")
def home():
    return jsonify({
        "message": "Bearer Token Demo",
        "use_token": "demo-secret-token"
    })


@app.route("/secret-data")
def secret():

    auth = request.headers.get("Authorization")

    if not auth:
        return jsonify({"error": "Missing Authorization header"}), 401

    if auth != f"Bearer {VALID_TOKEN}":
        return jsonify({"error": "Invalid token"}), 403

    return jsonify({
        "secret_data": "This is protected data"
    })


if __name__ == "__main__":
    app.run(debug=True)