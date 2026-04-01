from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

SECRET = "secret-key"


@app.route("/login_admin")
def login_admin():

    token = jwt.encode({
        "user": "admin",
        "role": "admin"
    }, SECRET, algorithm="HS256")

    return jsonify({"token": token})


@app.route("/login_user")
def login_user():

    token = jwt.encode({
        "user": "bob",
        "role": "user"
    }, SECRET, algorithm="HS256")

    return jsonify({"token": token})


@app.route("/admin-dashboard")
def admin_dashboard():

    token = request.headers.get("Authorization").split()[1]
    data = jwt.decode(token, SECRET, algorithms=["HS256"])

    if data["role"] != "admin":
        return jsonify({"error": "Admin only"}), 403

    return jsonify({
        "dashboard": "admin statistics"
    })


if __name__ == "__main__":
    app.run(debug=True)