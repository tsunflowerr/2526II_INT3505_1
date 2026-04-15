# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

ITEMS = {}
NEXT_ID = 1
TOKEN = "demo-token"


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    if data.get("username") == "admin" and data.get("password") == "123456":
        return jsonify({"token": TOKEN})
    return jsonify({"error": "invalid credentials"}), 401


@app.post("/items")
def create_item():
    global NEXT_ID
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {TOKEN}":
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400

    item = {"id": NEXT_ID, "name": name}
    ITEMS[NEXT_ID] = item
    NEXT_ID += 1
    return jsonify(item), 201


@app.get("/items/<int:item_id>")
def get_item(item_id):
    item = ITEMS.get(item_id)
    if not item:
        return jsonify({"error": "not found"}), 404
    return jsonify(item)


@app.delete("/items/<int:item_id>")
def delete_item(item_id):
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {TOKEN}":
        return jsonify({"error": "unauthorized"}), 401

    item = ITEMS.pop(item_id, None)
    if not item:
        return jsonify({"error": "not found"}), 404
    return jsonify({"deleted": True, "id": item_id})


if __name__ == "__main__":
    app.run(port=5000, debug=True)