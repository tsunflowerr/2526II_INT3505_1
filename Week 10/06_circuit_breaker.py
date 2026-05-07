from flask import Flask, jsonify
import time
import random
import os

app = Flask(__name__)

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=10):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.state = "closed"
        self.last_failure_time = None

    def call(self, func):
        if self.state == "open":
            if time.time() - self.last_failure_time < self.recovery_timeout:
                raise RuntimeError("circuit_open")
            self.state = "half_open"

        try:
            result = func()
            self.failures = 0
            self.state = "closed"
            return result
        except Exception:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = "open"
            raise

breaker = CircuitBreaker()

def unstable_payment_gateway():
    if random.random() < 0.7:
        raise RuntimeError("payment_gateway_failed")
    return {"provider": "demo_gateway", "status": "ok"}

@app.get("/api/v1/payment-provider-status")
def provider_status():
    try:
        result = breaker.call(unstable_payment_gateway)
        return jsonify(result=result, circuit_state=breaker.state)
    except RuntimeError as exc:
        return jsonify(error=str(exc), circuit_state=breaker.state), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
