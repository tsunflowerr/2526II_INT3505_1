# 06_performance_load_api.py
# Demo: Performance/load test đơn giản cho Flask API
# Chạy server: python 06_performance_load_api.py
# Chạy load test: python 06_performance_load_api.py load

from flask import Flask, jsonify
import sys
import time
import threading
import urllib.request
import json
from werkzeug.serving import make_server

app = Flask(__name__)


@app.get("/ping")
def ping():
    return jsonify({"message": "pong"})


@app.get("/work")
def work():
    time.sleep(0.05)  # giả lập xử lý 50ms
    return jsonify({"message": "done"})


class ServerThread(threading.Thread):
    def __init__(self, app):
        super().__init__(daemon=True)
        self.server = make_server("127.0.0.1", 5001, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


def call_api(results, index):
    start = time.perf_counter()
    with urllib.request.urlopen("http://127.0.0.1:5001/work") as response:
        body = json.loads(response.read().decode("utf-8"))
    end = time.perf_counter()
    results[index] = {
        "ok": body["message"] == "done",
        "latency_ms": round((end - start) * 1000, 2),
    }


def run_load_test(total_requests=20):
    server = ServerThread(app)
    server.start()
    time.sleep(0.3)

    threads = []
    results = [None] * total_requests
    started = time.perf_counter()

    for i in range(total_requests):
        t = threading.Thread(target=call_api, args=(results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    finished = time.perf_counter()
    server.shutdown()

    latencies = [r["latency_ms"] for r in results if r and r["ok"]]
    print("total_requests =", total_requests)
    print("success =", len(latencies))
    print("total_time_ms =", round((finished - started) * 1000, 2))
    print("avg_latency_ms =", round(sum(latencies) / len(latencies), 2))
    print("max_latency_ms =", max(latencies))
    print("min_latency_ms =", min(latencies))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "load":
        run_load_test()
    else:
        app.run(debug=True)