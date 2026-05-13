# demos/crud.py
from flask import Blueprint, jsonify, request

crud_bp = Blueprint("crud", __name__, url_prefix="/crud")

products = {
    1: {"id": 1, "name": "Laptop", "price": 1500},
    2: {"id": 2, "name": "Mouse", "price": 20},
}


@crud_bp.get("/products")
def get_products():
    return jsonify(list(products.values()))


@crud_bp.get("/products/<int:product_id>")
def get_product(product_id):
    product = products.get(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product)


@crud_bp.post("/products")
def create_product():
    data = request.get_json()

    product_id = max(products.keys()) + 1
    product = {
        "id": product_id,
        "name": data["name"],
        "price": data["price"]
    }

    products[product_id] = product

    return jsonify(product), 201


@crud_bp.put("/products/<int:product_id>")
def update_product(product_id):
    if product_id not in products:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()

    products[product_id]["name"] = data.get("name", products[product_id]["name"])
    products[product_id]["price"] = data.get("price", products[product_id]["price"])

    return jsonify(products[product_id])


@crud_bp.delete("/products/<int:product_id>")
def delete_product(product_id):
    if product_id not in products:
        return jsonify({"error": "Product not found"}), 404

    deleted_product = products.pop(product_id)

    return jsonify({
        "message": "Product deleted",
        "product": deleted_product
    })