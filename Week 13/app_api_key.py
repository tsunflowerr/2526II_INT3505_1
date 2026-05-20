from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

developers = {}

@app.route("/")
def home():
    return """
    <h1>Developer Registration</h1>
    <p>POST /register với JSON: {"name": "Alice", "email": "alice@example.com"}</p>
    """

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    api_key = str(uuid.uuid4())

    developers[api_key] = {
        "name": name,
        "email": email
    }

    return jsonify({
        "message": "Developer registered successfully",
        "api_key": api_key
    })

@app.route("/api/profile")
def profile():
    api_key = request.headers.get("X-API-Key")

    if api_key not in developers:
        return jsonify({"error": "Invalid API key"}), 401

    return jsonify({
        "developer": developers[api_key],
        "message": "API key is valid"
    })

if __name__ == "__main__":
    app.run(debug=True)
