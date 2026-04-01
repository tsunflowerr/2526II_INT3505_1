from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

SECRET_KEY = "super-secret-key"


def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


@app.route("/profile")
def profile():

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"error": "Missing Authorization header"}), 401

    try:
        token = auth_header.split()[1]
    except:
        return jsonify({"error": "Invalid Authorization format"}), 401

    user_data = verify_token(token)

    if not user_data:
        return jsonify({"error": "Invalid or expired token"}), 401

    return jsonify({
        "message": "Access granted",
        "user": user_data["username"]
    })


if __name__ == "__main__":
    app.run(debug=True)