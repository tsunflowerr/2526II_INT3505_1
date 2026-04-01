from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

SECRET = "secret-key"


@app.route("/login")
def login():

    token = jwt.encode({
        "user": "alice",
        "scopes": ["read"]
    }, SECRET, algorithm="HS256")

    return jsonify({
        "token": token,
        "scopes": ["read"]
    })


@app.route("/read-data")
def read_data():

    token = request.headers.get("Authorization").split()[1]
    data = jwt.decode(token, SECRET, algorithms=["HS256"])

    if "read" not in data["scopes"]:
        return jsonify({"error": "Missing read scope"}), 403

    return jsonify({"data": "public report"})


@app.route("/write-data")
def write_data():

    token = request.headers.get("Authorization").split()[1]
    data = jwt.decode(token, SECRET, algorithms=["HS256"])

    if "write" not in data["scopes"]:
        return jsonify({"error": "Missing write scope"}), 403

    return jsonify({"status": "write success"})


if __name__ == "__main__":
    app.run(debug=True)