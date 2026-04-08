from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {"_id": "6612abc123", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 22},
    {"_id": "6612abc124", "name": "Tran Thi B", "email": "b@gmail.com", "age": 21},
]


@app.get("/health")
def health_check():
    return jsonify({"status": "ok"})


@app.get("/users/sample-document")
def get_sample_document():
    return jsonify(users[0])


@app.get("/users")
def get_users():
    return jsonify(users)


if __name__ == "__main__":
    app.run(debug=True)
