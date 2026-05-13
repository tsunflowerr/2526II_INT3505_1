# demos/rest.py
from flask import Blueprint, jsonify, request

rest_bp = Blueprint("rest", __name__, url_prefix="/rest")

users = {
    1: {
        "id": 1,
        "name": "An",
        "email": "an@example.com"
    },
    2: {
        "id": 2,
        "name": "Binh",
        "email": "binh@example.com"
    }
}


@rest_bp.get("/users")
def get_users():
    return jsonify(list(users.values()))


@rest_bp.get("/users/<int:user_id>")
def get_user(user_id):
    user = users.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)


@rest_bp.post("/users")
def create_user():
    data = request.get_json()

    user_id = max(users.keys()) + 1

    user = {
        "id": user_id,
        "name": data["name"],
        "email": data["email"]
    }

    users[user_id] = user

    return jsonify(user), 201