# 02_unit_validation_api.py
# Demo: Unit test validate input request
# Chạy API:   python 02_unit_validation_api.py
# Chạy test:  python 02_unit_validation_api.py test

from flask import Flask, jsonify, request
import sys
import unittest

app = Flask(__name__)


def validate_create_user(data):
    if not isinstance(data, dict):
        return "body must be json"
    if not data.get("name"):
        return "name is required"
    age = data.get("age")
    if not isinstance(age, int) or age < 0:
        return "age must be a non-negative integer"
    return None


@app.post("/users")
def create_user():
    data = request.get_json(silent=True) or {}
    error = validate_create_user(data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "user created", "user": data}), 201


class ValidationUnitTest(unittest.TestCase):
    def test_valid_user(self):
        self.assertIsNone(validate_create_user({"name": "An", "age": 20}))

    def test_missing_name(self):
        self.assertEqual(
            validate_create_user({"age": 20}),
            "name is required",
        )

    def test_invalid_age(self):
        self.assertEqual(
            validate_create_user({"name": "An", "age": -1}),
            "age must be a non-negative integer",
        )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[sys.argv[0]])
    else:
        app.run(debug=True)