from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def developer_portal():
    return """
    <h1>Weather API Developer Portal</h1>
    <p>API cung cấp dữ liệu thời tiết demo cho developer.</p>

    <h2>Quick Start</h2>
    <pre>GET /api/weather?city=Hanoi</pre>

    <h2>Endpoints</h2>
    <ul>
        <li>GET /api/weather?city=Hanoi</li>
        <li>GET /api/docs</li>
    </ul>
    """

@app.route("/api/docs")
def docs():
    return jsonify({
        "name": "Weather API",
        "version": "1.0",
        "endpoints": [
            {
                "method": "GET",
                "path": "/api/weather?city=Hanoi",
                "description": "Lấy thông tin thời tiết theo thành phố"
            }
        ]
    })

@app.route("/api/weather")
def weather():
    return jsonify({
        "city": "Hanoi",
        "temperature": 30,
        "condition": "Sunny"
    })

if __name__ == "__main__":
    app.run(debug=True)
