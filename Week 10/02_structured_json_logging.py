from flask import Flask, jsonify, request, g
import logging
import json
import time
import uuid
import os

app = Flask(__name__)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "level": record.levelname,
            "message": record.getMessage(),
            "time": self.formatTime(record),
            "logger": record.name,
        }
        if hasattr(record, "extra_data"):
            payload.update(record.extra_data)
        return json.dumps(payload, ensure_ascii=False)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
app.logger.handlers.clear()
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.before_request
def start_request():
    g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    g.start_time = time.time()

@app.after_request
def log_request(response):
    duration_ms = round((time.time() - g.start_time) * 1000, 2)
    app.logger.info("request_completed", extra={"extra_data": {
        "request_id": g.request_id,
        "method": request.method,
        "path": request.path,
        "status_code": response.status_code,
        "duration_ms": duration_ms,
        "remote_addr": request.remote_addr,
    }})
    response.headers["X-Request-ID"] = g.request_id
    return response

@app.get("/api/v1/orders/<int:order_id>")
def get_order(order_id):
    app.logger.info("order_viewed", extra={"extra_data": {"request_id": g.request_id, "order_id": order_id}})
    return jsonify(id=order_id, total=199000, currency="VND")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
