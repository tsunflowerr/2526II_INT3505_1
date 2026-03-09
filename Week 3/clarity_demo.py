from flask import Flask, jsonify

app = Flask(__name__)

# Endpoint rõ ràng, dễ hiểu
@app.route("/users")
def get_users():
    return jsonify(["An", "Binh", "Cuong"])

# Endpoint rõ ràng: lấy user theo id
@app.route("/users/<int:id>")
def get_user(id):
    return jsonify({"id": id, "name": "An"})

app.run()