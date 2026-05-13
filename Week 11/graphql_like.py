# demos/graphql_like.py
from flask import Blueprint, jsonify, request

graphql_bp = Blueprint("graphql_like", __name__, url_prefix="/graphql")

users = {
    1: {
        "id": 1,
        "name": "An",
        "email": "an@example.com",
        "age": 20
    },
    2: {
        "id": 2,
        "name": "Binh",
        "email": "binh@example.com",
        "age": 21
    }
}


@graphql_bp.post("")
def graphql_query():
    body = request.get_json()

    user_id = body.get("user_id")
    fields = body.get("fields", [])

    user = users.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    result = {}

    for field in fields:
        if field in user:
            result[field] = user[field]

    return jsonify({
        "data": {
            "user": result
        }
    })