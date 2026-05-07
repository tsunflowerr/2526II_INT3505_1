from flask import Flask, jsonify, request, Response
import time
import os

app = Flask(__name__)
REQUEST_COUNT = {}
REQUEST_LATENCY = {}

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    key = (request.method, request.path, response.status_code)
    REQUEST_COUNT[key] = REQUEST_COUNT.get(key, 0) + 1
    REQUEST_LATENCY.setdefault(request.path, []).append(time.time() - request.start_time)
    return response

@app.get("/api/v1/products")
def products():
    time.sleep(0.05)
    return jsonify(items=[{"id": 1, "name": "Keyboard"}, {"id": 2, "name": "Mouse"}])

@app.get("/metrics")
def metrics():
    lines = []
    lines.append("# HELP flask_http_requests_total Total HTTP requests")
    lines.append("# TYPE flask_http_requests_total counter")
    for (method, path, status), count in REQUEST_COUNT.items():
        lines.append(f'flask_http_requests_total{{method="{method}",path="{path}",status="{status}"}} {count}')

    lines.append("# HELP flask_http_request_duration_seconds_avg Average request latency")
    lines.append("# TYPE flask_http_request_duration_seconds_avg gauge")
    for path, values in REQUEST_LATENCY.items():
        avg = sum(values) / len(values)
        lines.append(f'flask_http_request_duration_seconds_avg{{path="{path}"}} {avg}')
    return Response("\n".join(lines) + "\n", mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
