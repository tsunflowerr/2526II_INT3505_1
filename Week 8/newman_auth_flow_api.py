from flask import Flask, jsonify, request
import sys
import unittest

app = Flask(__name__)

VALID_USER = {"username": "admin", "password": "123456"}
VALID_TOKEN = "demo-token-123"


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    if (
        data.get("username") == VALID_USER["username"]
        and data.get("password") == VALID_USER["password"]
    ):
        return jsonify({"token": VALID_TOKEN})
    return jsonify({"error": "invalid credentials"}), 401


@app.get("/profile")
def profile():
    auth_header = request.headers.get("Authorization", "")
    if auth_header != f"Bearer {VALID_TOKEN}":
        return jsonify({"error": "unauthorized"}), 401
    return jsonify({"username": "admin", "role": "tester"})


class NewmanStyleFlowTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_login_success_then_get_profile(self):
        login_res = self.client.post(
            "/login",
            json={"username": "admin", "password": "123456"},
        )
        self.assertEqual(login_res.status_code, 200)
        token = login_res.get_json()["token"]

        profile_res = self.client.get(
            "/profile",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(profile_res.status_code, 200)
        self.assertEqual(profile_res.get_json()["role"], "tester")

    def test_login_fail(self):
        res = self.client.post(
            "/login",
            json={"username": "admin", "password": "wrong"},
        )
        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[sys.argv[0]])
    else:
        app.run(debug=True)