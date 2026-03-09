from flask import Flask, jsonify

app = Flask(__name__)

# V1: API ban đầu - chỉ có id và name
@app.route("/v1/users")
def get_users_v1():
    return jsonify([
        {"id": 1, "name": "An"},
        {"id": 2, "name": "Binh"}
    ])

# V2: Mở rộng thêm field email - không ảnh hưởng V1
@app.route("/v2/users")
def get_users_v2():
    return jsonify([
        {"id": 1, "name": "An", "email": "an@gmail.com"},
        {"id": 2, "name": "Binh", "email": "binh@gmail.com"}
    ])

app.run(debug=True)