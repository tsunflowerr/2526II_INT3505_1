from flask import Flask, jsonify, request
import time
import os

app = Flask(__name__)
WINDOW_SECONDS = 60
MAX_REQUESTS = 5
BUCKETS = {}

def client_key():
    return request.headers.get("X-API-Key") or request.remote_addr or "anonymous"

@app.before_request
def rate_limit():
    now = time.time()
    key = client_key()
    bucket = [ts for ts in BUCKETS.get(key, []) if now - ts < WINDOW_SECONDS]

    if len(bucket) >= MAX_REQUESTS:
        retry_after = int(WINDOW_SECONDS - (now - bucket[0]))
        return jsonify(error="rate_limit_exceeded", retry_after_seconds=retry_after), 429

    bucket.append(now)
    BUCKETS[key] = bucket

@app.get("/api/v1/payments")
def payments():
    return jsonify(items=[{"id": "pay_001", "amount": 150000}])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
