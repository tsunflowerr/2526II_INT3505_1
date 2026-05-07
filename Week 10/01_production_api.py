from flask import Flask, jsonify, request
import os

app = Flask(__name__)
app.config["ENV_NAME"] = os.getenv("ENV_NAME", "production")
app.config["API_VERSION"] = os.getenv("API_VERSION", "v1")

@app.get("/health")
def health():
    return jsonify(status="ok", env=app.config["ENV_NAME"])

@app.get("/api/v1/users/<int:user_id>")
def get_user(user_id):
    return jsonify(id=user_id, name=f"User {user_id}", version=app.config["API_VERSION"])

@app.errorhandler(404)
def not_found(error):
    return jsonify(error="not_found", path=request.path), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify(error="internal_server_error"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
