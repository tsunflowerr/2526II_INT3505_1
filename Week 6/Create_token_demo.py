from flask import Flask, jsonify
import jwt
import datetime

app = Flask(__name__)

SECRET_KEY = "super-secret-key"

@app.route("/")
def home():
    return jsonify({
        "message": "JWT Token Creation Demo",
        "endpoint": "/login"
    })


@app.route("/login")
def login():
    payload = {
        "user_id": 1,
        "username": "alice",
        "role": "user",

        "iat": datetime.datetime.utcnow(),

        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "message": "Login success",
        "token": token,
        "token_structure": "HEADER.PAYLOAD.SIGNATURE"
    })


if __name__ == "__main__":
    app.run(debug=True)