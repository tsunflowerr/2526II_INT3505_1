from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.get("/api/v1/profile")
def profile_v1():
    response = make_response(jsonify({
        "id": 1,
        "name": "Thanh",
        "note": "Please move to /api/v2/profile"
    }))
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = "Tue, 30 Jun 2026 23:59:59 GMT"
    response.headers["Link"] = '</api/v2/profile>; rel="successor-version"'
    return response

@app.get("/api/v2/profile")
def profile_v2():
    return jsonify({
        "id": 1,
        "full_name": "Tran Quang Thanh",
        "email": "thanh@example.com"
    })

if __name__ == "__main__":
    app.run(debug=True)