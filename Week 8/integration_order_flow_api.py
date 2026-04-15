from flask import Flask, jsonify, request
import sys
import unittest

app = Flask(__name__)


class OrderRepository:
    def __init__(self):
        self.orders = {}
        self.current_id = 1

    def create(self, item, qty):
        order = {"id": self.current_id, "item": item, "qty": qty}
        self.orders[self.current_id] = order
        self.current_id += 1
        return order

    def get(self, order_id):
        return self.orders.get(order_id)


repo = OrderRepository()


def create_order(data):
    item = data.get("item")
    qty = data.get("qty")
    if not item:
        return None, "item is required"
    if not isinstance(qty, int) or qty <= 0:
        return None, "qty must be a positive integer"
    return repo.create(item, qty), None


@app.post("/orders")
def create_order_api():
    data = request.get_json(silent=True) or {}
    order, error = create_order(data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(order), 201


@app.get("/orders/<int:order_id>")
def get_order_api(order_id):
    order = repo.get(order_id)
    if not order:
        return jsonify({"error": "order not found"}), 404
    return jsonify(order)


class OrderFlowIntegrationTest(unittest.TestCase):
    def setUp(self):
        global repo
        repo = OrderRepository()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_create_then_get_order(self):
        create_res = self.client.post("/orders", json={"item": "book", "qty": 2})
        self.assertEqual(create_res.status_code, 201)

        order_id = create_res.get_json()["id"]
        get_res = self.client.get(f"/orders/{order_id}")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.get_json()["item"], "book")

    def test_create_order_invalid_qty(self):
        res = self.client.post("/orders", json={"item": "book", "qty": 0})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()["error"], "qty must be a positive integer")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[sys.argv[0]])
    else:
        app.run(debug=True)