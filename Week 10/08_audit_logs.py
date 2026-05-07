from flask import Flask, jsonify, request, g
import json
import time
import uuid
import os

app = Flask(__name__)
AUDIT_FILE = os.getenv("AUDIT_FILE", "audit.log")

@app.before_request
def identify_actor():
    g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    g.actor = request.headers.get("X-User-ID", "anonymous")


def write_audit(action, resource, status):
    event = {
        "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "request_id": g.request_id,
        "actor": g.actor,
        "action": action,
        "resource": resource,
        "status": status,
        "ip": request.remote_addr,
    }
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

@app.post("/api/v1/admin/users/<int:user_id>/lock")
def lock_user(user_id):
    write_audit(action="lock_user", resource=f"user:{user_id}", status="success")
    return jsonify(status="locked", user_id=user_id)

@app.get("/api/v1/audit-demo")
def audit_demo():
    write_audit(action="view_audit_demo", resource="audit-demo", status="success")
    return jsonify(message="audit event written")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
