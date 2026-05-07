from flask import Flask, jsonify, request, g
import json
import logging
import os
import re
import time
import uuid

app = Flask(__name__)
RATE_LIMIT_WINDOW = 60
RATE_LIMIT_MAX = 10
RATE_BUCKETS = {}
REQUEST_TOTAL = {}
LATENCIES = []
WAF_PATTERNS = [re.compile(r"<script", re.I), re.compile(r"union\s+select", re.I)]

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {"time": self.formatTime(record), "level": record.levelname, "message": record.getMessage()}
        if hasattr(record, "extra_data"):
            payload.update(record.extra_data)
        return json.dumps(payload, ensure_ascii=False)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
app.logger.handlers.clear()
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.before_request
def before_request():
    g.start_time = time.time()
    g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    g.actor = request.headers.get("X-User-ID", "anonymous")

    raw = request.query_string.decode(errors="ignore") + " " + request.get_data(as_text=True)
    if any(pattern.search(raw) for pattern in WAF_PATTERNS):
        audit("blocked_request", request.path, "blocked")
        return jsonify(error="blocked_by_waf"), 403

    key = request.headers.get("X-API-Key") or request.remote_addr or "anonymous"
    now = time.time()
    bucket = [ts for ts in RATE_BUCKETS.get(key, []) if now - ts < RATE_LIMIT_WINDOW]
    if len(bucket) >= RATE_LIMIT_MAX:
        audit("rate_limit", request.path, "blocked")
        return jsonify(error="rate_limit_exceeded"), 429
    bucket.append(now)
    RATE_BUCKETS[key] = bucket

@app.after_request
def after_request(response):
    duration = time.time() - g.start_time
    REQUEST_TOTAL[(request.method, request.path, response.status_code)] = REQUEST_TOTAL.get((request.method, request.path, response.status_code), 0) + 1
    LATENCIES.append(duration)

    app.logger.info("request_completed", extra={"extra_data": {
        "request_id": g.request_id,
        "actor": g.actor,
        "method": request.method,
        "path": request.path,
        "status": response.status_code,
        "duration_ms": round(duration * 1000, 2),
    }})

    response.headers["X-Request-ID"] = g.request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response

def audit(action, resource, status):
    event = {
        "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "request_id": getattr(g, "request_id", None),
        "actor": getattr(g, "actor", "anonymous"),
        "action": action,
        "resource": resource,
        "status": status,
    }
    with open("audit.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

@app.get("/api/v1/invoices/<int:invoice_id>")
def invoice(invoice_id):
    audit("view_invoice", f"invoice:{invoice_id}", "success")
    return jsonify(id=invoice_id, amount=450000, currency="VND")

@app.get("/metrics")
def metrics():
    lines = ["# TYPE http_requests_total counter"]
    for (method, path, status), count in REQUEST_TOTAL.items():
        lines.append(f'http_requests_total{{method="{method}",path="{path}",status="{status}"}} {count}')
    avg = sum(LATENCIES) / len(LATENCIES) if LATENCIES else 0
    lines.append("# TYPE http_request_duration_seconds_avg gauge")
    lines.append(f"http_request_duration_seconds_avg {avg}")
    return "\n".join(lines) + "\n", 200, {"Content-Type": "text/plain"}

@app.get("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
