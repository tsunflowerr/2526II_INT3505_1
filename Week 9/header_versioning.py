from flask import Flask, jsonify, request

app = Flask(__name__)

user = {"id": 1, "name": "Thanh", "email": "thanh@example.com"}

@app.get("/api/user")
def get_user():
    version = request.headers.get("X-API-Version", "1")

    if version == "2":
        return jsonify({
            "id": user["id"],
            "full_name": user["name"],
            "email": user["email"],
            "active": True
        })

    return jsonify(user)

if __name__ == "__main__":
    app.run(debug=True)