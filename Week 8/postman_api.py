# 04_postman_crud_api.py
# Demo: API CRUD đơn giản để test bằng Postman
# Chạy: python 04_postman_crud_api.py

from flask import Flask, jsonify, request

app = Flask(__name__)

products = {}
current_id = 1


@app.get("/products")
def list_products():
    return jsonify(list(products.values()))


@app.post("/products")
def create_product():
    global current_id
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    price = data.get("price")

    if not name:
        return jsonify({"error": "name is required"}), 400
    if not isinstance(price, (int, float)) or price < 0:
        return jsonify({"error": "price must be >= 0"}), 400

    product = {"id": current_id, "name": name, "price": price}
    products[current_id] = product
    current_id += 1
    return jsonify(product), 201


@app.get("/products/<int:product_id>")
def get_product(product_id):
    product = products.get(product_id)
    if not product:
        return jsonify({"error": "product not found"}), 404
    return jsonify(product)


@app.put("/products/<int:product_id>")
def update_product(product_id):
    product = products.get(product_id)
    if not product:
        return jsonify({"error": "product not found"}), 404

    data = request.get_json(silent=True) or {}
    if "name" in data:
        if not data["name"]:
            return jsonify({"error": "name cannot be empty"}), 400
        product["name"] = data["name"]

    if "price" in data:
        if not isinstance(data["price"], (int, float)) or data["price"] < 0:
            return jsonify({"error": "price must be >= 0"}), 400
        product["price"] = data["price"]

    return jsonify(product)


@app.delete("/products/<int:product_id>")
def delete_product(product_id):
    if product_id not in products:
        return jsonify({"error": "product not found"}), 404
    deleted = products.pop(product_id)
    return jsonify(deleted)


if __name__ == "__main__":
    app.run(debug=True)