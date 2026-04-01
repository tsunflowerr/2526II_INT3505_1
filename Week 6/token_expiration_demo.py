from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

SECRET = "secret-key"


@app.route("/login")
def login():

    token = jwt.encode({
        "user": "alice",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=15)
    }, SECRET, algorithm="HS256")

    return jsonify({
        "token": token,
        "note": "Token expires in 15 seconds"
    })


@app.route("/protected")
def protected():

    auth = request.headers.get("Authorization")

    if not auth:
        return jsonify({"error": "Missing token"}), 401

    token = auth.split()[1]

    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])

        return jsonify({
            "message": "Access granted",
            "user": decoded["user"]
        })

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401

    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


if __name__ == "__main__":
    app.run(debug=True)