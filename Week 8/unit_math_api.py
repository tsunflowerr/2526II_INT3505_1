# 01_unit_math_api.py
# Demo: Unit test cơ bản cho business logic tách riêng khỏi API
# Chạy API:   python 01_unit_math_api.py
# Chạy test:  python 01_unit_math_api.py test

from flask import Flask, jsonify, request
import sys
import unittest

app = Flask(__name__)


def add(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("a and b must be numbers")
    return a + b


@app.get("/sum")
def sum_api():
    try:
        a = float(request.args.get("a", "0"))
        b = float(request.args.get("b", "0"))
        return jsonify({"result": add(a, b)})
    except ValueError:
        return jsonify({"error": "a and b must be numbers"}), 400


class AddUnitTest(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_floats(self):
        self.assertEqual(add(1.5, 2.5), 4.0)

    def test_add_invalid_type(self):
        with self.assertRaises(TypeError):
            add("2", 3)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[sys.argv[0]])
    else:
        app.run(debug=True)