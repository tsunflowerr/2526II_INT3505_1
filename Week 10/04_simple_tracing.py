from flask import Flask, jsonify, request, g
import time
import uuid
import os

app = Flask(__name__)

class Span:
    def __init__(self, name):
        self.name = name
        self.start = time.time()
        self.end = None

    def finish(self):
        self.end = time.time()
        return {"name": self.name, "duration_ms": round((self.end - self.start) * 1000, 2)}

@app.before_request
def start_trace():
    g.trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
    g.spans = [Span(f"HTTP {request.method} {request.path}")]

@app.after_request
def end_trace(response):
    trace = {
        "trace_id": g.trace_id,
        "spans": [span.finish() for span in g.spans],
        "status_code": response.status_code,
    }
    print(trace, flush=True)
    response.headers["X-Trace-ID"] = g.trace_id
    return response

def query_database():
    span = Span("database.query")
    time.sleep(0.03)
    g.spans.append(span)
    return {"id": 1, "name": "Inventory service"}

@app.get("/api/v1/service-info")
def service_info():
    data = query_database()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
