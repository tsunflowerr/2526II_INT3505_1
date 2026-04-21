from flask import Flask, jsonify, request

app = Flask(__name__)

@app.post("/api/v1/register")
def register_v1():
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400
    return jsonify({"message": f"registered {name}"})

@app.post("/api/v2/register")
def register_v2():
    data = request.get_json() or {}
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    if not first_name or not last_name:
        return jsonify({"error": "first_name and last_name are required"}), 400

    return jsonify({
        "message": "registered",
        "user": {
            "first_name": first_name,
            "last_name": last_name
        }
    })

if __name__ == "__main__":
    app.run(debug=True)