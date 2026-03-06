from flask import Flask, jsonify, make_response, request
import random

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "OK", "message": "Server đang chạy!"})

user = [
    {
        "id": 1,
        "name": "Alice",
    },
    {
        "id": 2,
        "name": "Bob",
    },
]

@app.route("/users", methods=["GET"])    
def get_users():
    return jsonify(user)

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    for u in user:
        if u["id"] == user_id:
            return jsonify(u)
    return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=["POST"])
def create_user():
    new_user = {
        "id": len(user) + 1,
        "name": f"User{len(user) + 1}"
    }
    user.append(new_user)
    return jsonify(new_user), 201


@app.route("/sum", methods=["POST"])
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
