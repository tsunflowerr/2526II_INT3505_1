# run_newman.py
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).parent
COLLECTION_FILE = BASE_DIR / "postman_collection.json"
ENV_FILE = BASE_DIR / "postman_environment.json"


def write_postman_files():
    collection = {
        "info": {
            "name": "Flask 5 Endpoints Demo",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": [
            {
                "name": "1. Health",
                "request": {
                    "method": "GET",
                    "header": [],
                    "url": {
                        "raw": "{{base_url}}/health",
                        "host": ["{{base_url}}"],
                        "path": ["health"],
                    },
                },
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "type": "text/javascript",
                            "exec": [
                                "pm.test('status 200', function () { pm.response.to.have.status(200); });",
                                "pm.test('status ok', function () { pm.expect(pm.response.json().status).to.eql('ok'); });",
                            ],
                        },
                    }
                ],
            },
            {
                "name": "2. Login",
                "request": {
                    "method": "POST",
                    "header": [{"key": "Content-Type", "value": "application/json"}],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({"username": "admin", "password": "123456"}),
                    },
                    "url": {
                        "raw": "{{base_url}}/login",
                        "host": ["{{base_url}}"],
                        "path": ["login"],
                    },
                },
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "type": "text/javascript",
                            "exec": [
                                "pm.test('status 200', function () { pm.response.to.have.status(200); });",
                                "var data = pm.response.json();",
                                "pm.environment.set('token', data.token);",
                                "pm.test('token exists', function () { pm.expect(data.token).to.be.a('string'); });",
                            ],
                        },
                    }
                ],
            },
            {
                "name": "3. Create Item",
                "request": {
                    "method": "POST",
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                        {"key": "Authorization", "value": "Bearer {{token}}"},
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({"name": "book"}),
                    },
                    "url": {
                        "raw": "{{base_url}}/items",
                        "host": ["{{base_url}}"],
                        "path": ["items"],
                    },
                },
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "type": "text/javascript",
                            "exec": [
                                "pm.test('status 201', function () { pm.response.to.have.status(201); });",
                                "var data = pm.response.json();",
                                "pm.environment.set('item_id', data.id);",
                                "pm.test('item name correct', function () { pm.expect(data.name).to.eql('book'); });",
                            ],
                        },
                    }
                ],
            },
            {
                "name": "4. Get Item",
                "request": {
                    "method": "GET",
                    "header": [],
                    "url": {
                        "raw": "{{base_url}}/items/{{item_id}}",
                        "host": ["{{base_url}}"],
                        "path": ["items", "{{item_id}}"],
                    },
                },
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "type": "text/javascript",
                            "exec": [
                                "pm.test('status 200', function () { pm.response.to.have.status(200); });",
                                "var data = pm.response.json();",
                                "pm.test('item id exists', function () { pm.expect(data.id).to.exist; });",
                                "pm.test('item name correct', function () { pm.expect(data.name).to.eql('book'); });",
                            ],
                        },
                    }
                ],
            },
            {
                "name": "5. Delete Item",
                "request": {
                    "method": "DELETE",
                    "header": [
                        {"key": "Authorization", "value": "Bearer {{token}}"},
                    ],
                    "url": {
                        "raw": "{{base_url}}/items/{{item_id}}",
                        "host": ["{{base_url}}"],
                        "path": ["items", "{{item_id}}"],
                    },
                },
                "event": [
                    {
                        "listen": "test",
                        "script": {
                            "type": "text/javascript",
                            "exec": [
                                "pm.test('status 200', function () { pm.response.to.have.status(200); });",
                                "var data = pm.response.json();",
                                "pm.test('deleted true', function () { pm.expect(data.deleted).to.eql(true); });",
                            ],
                        },
                    }
                ],
            },
        ],
    }

    environment = {
        "name": "local",
        "values": [
            {"key": "base_url", "value": "http://127.0.0.1:5000", "enabled": True},
            {"key": "token", "value": "", "enabled": True},
            {"key": "item_id", "value": "", "enabled": True},
        ],
    }

    COLLECTION_FILE.write_text(json.dumps(collection, indent=2), encoding="utf-8")
    ENV_FILE.write_text(json.dumps(environment, indent=2), encoding="utf-8")


def wait_for_server():
    import urllib.request

    url = "http://127.0.0.1:5000/health"
    for _ in range(30):
        try:
            with urllib.request.urlopen(url, timeout=1) as resp:
                if resp.status == 200:
                    return
        except Exception:
            time.sleep(0.5)
    raise RuntimeError("Flask server did not start")


def main():
    if shutil.which("newman") is None:
        raise RuntimeError("Newman chưa được cài. Cài bằng: npm install -g newman")

    write_postman_files()

    server = subprocess.Popen([sys.executable, "app.py"], cwd=BASE_DIR)
    try:
        wait_for_server()
        subprocess.run(
            [
                "newman",
                "run",
                str(COLLECTION_FILE),
                "-e",
                str(ENV_FILE),
            ],
            cwd=BASE_DIR,
            check=True,
        )
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()


if __name__ == "__main__":
    main()