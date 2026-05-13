# demos/grpc_like.py
from flask import Blueprint, jsonify, request

grpc_bp = Blueprint("grpc_like", __name__, url_prefix="/grpc")

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


@grpc_bp.post("/UserService/GetUser")
def get_user_rpc():
    data = request.get_json()

    user_id = data["user_id"]

    user = users.get(user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify({
        "response": user
    })


@grpc_bp.post("/UserService/CreateUser")
def create_user_rpc():
    data = request.get_json()

    user_id = max(users.keys()) + 1

    user = {
        "id": user_id,
        "name": data["name"],
        "email": data["email"]
    }

    users[user_id] = user

    return jsonify({
        "response": user
    })