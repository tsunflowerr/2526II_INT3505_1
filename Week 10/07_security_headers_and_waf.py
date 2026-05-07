from flask import Flask, jsonify, request
import re
import os

app = Flask(__name__)
BLOCK_PATTERNS = [
    re.compile(r"(<script|</script>)", re.IGNORECASE),
    re.compile(r"(union\s+select|drop\s+table)", re.IGNORECASE),
    re.compile(r"(\.\./|\.\.\\\\)"),
]

@app.before_request
def simple_waf():
    raw = request.query_string.decode("utf-8", errors="ignore") + " " + (request.get_data(as_text=True) or "")
    for pattern in BLOCK_PATTERNS:
        if pattern.search(raw):
            return jsonify(error="blocked_by_waf"), 403

@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

@app.get("/api/v1/search")
def search():
    q = request.args.get("q", "")
    return jsonify(query=q, results=[])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
