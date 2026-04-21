from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.get("/api/v1/status")
def status_v1():
    response = make_response(jsonify({
        "status": "ok",
        "deprecated": True,
        "message": "Use /api/v2/status"
    }))
    response.headers["Warning"] = '299 - "This API version is deprecated"'
    return response

@app.get("/api/v2/status")
def status_v2():
    return jsonify({
        "status": "ok",
        "version": "v2",
        "server_time": "2026-04-21T10:00:00Z"
    })

if __name__ == "__main__":
    app.run(debug=True)