from flask import Flask, jsonify, request, abort

app = Flask(__name__)

@app.get("/users")
def get_users():
    return jsonify({
        "data": [
            {"id": 1, "name": "Nguyễn Văn A"},
            {"id": 2, "name": "Trần Thị B"}
        ]
    })

@app.post("/users")
def create_user():
    name = request.json.get("name")
    if not name:
        return jsonify({"error": "Tên không được để trống"}), 400
    return jsonify({
        "message": "Tạo người dùng thành công",
        "data": {"id": 3, "name": name}
    }), 201

if __name__ == "__main__":
    app.run(debug=True)