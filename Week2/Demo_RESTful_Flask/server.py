from flask import Flask, jsonify, make_response, request
import random
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

SECRET_KEY = "mysecretkey"

# JWT decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({"error": "Token is invalid"}), 401

        return f(*args, **kwargs)

    return decorated


@app.route("/health")
def health():
    return jsonify({"status": "OK", "message": "Server đang chạy!"})


users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]


# LOGIN -> trả JWT
@app.route("/login", methods=["POST"])
def login():

    data = request.json
    username = data.get("username")

    if not username:
        return {"error": "Missing username"}, 400

    token = jwt.encode(
        {
            "user": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"token": token})


# Protected route
@app.route("/users", methods=["GET"])
@token_required
def get_users():
    return jsonify(users)


@app.route("/users/<int:user_id>", methods=["GET"])
@token_required
def get_user(user_id):
    for u in users:
        if u["id"] == user_id:
            return jsonify(u)
    return jsonify({"error": "User not found"}), 404


@app.route("/users", methods=["POST"])
@token_required
def create_user():
    new_user = {
        "id": len(users) + 1,
        "name": f"User{len(users) + 1}"
    }
    users.append(new_user)
    return jsonify(new_user), 201


@app.route("/sum", methods=["POST"])
@token_required
def calculate_sum():
    data = request.json

    a = data.get("a")
    b = data.get("b")

    if a is None or b is None:
        return {"error": "Missing data"}, 400

    return jsonify({
        "a": a,
        "b": b,
        "sum": a + b
    })


@app.route("/random")
def get_random():
    resp = make_response(jsonify({"number": random.randint(1, 1000)}))
    resp.headers["Cache-Control"] = "max-age=10"
    return resp


if __name__ == "__main__":
    app.run(port=5000, debug=True)