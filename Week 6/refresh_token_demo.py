from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

SECRET = "secret-key"

refresh_store = {}


@app.route("/login")
def login():

    user = "alice"

    access_token = jwt.encode({
        "user": user,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=20)
    }, SECRET, algorithm="HS256")

    refresh_token = jwt.encode({
        "user": user
    }, SECRET, algorithm="HS256")

    refresh_store[refresh_token] = user

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    })


@app.route("/refresh")
def refresh():

    refresh_token = request.args.get("token")

    if refresh_token not in refresh_store:
        return jsonify({"error": "Invalid refresh token"}), 401

    new_access = jwt.encode({
        "user": refresh_store[refresh_token],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=20)
    }, SECRET, algorithm="HS256")

    return jsonify({
        "new_access_token": new_access
    })


if __name__ == "__main__":
    app.run(debug=True)