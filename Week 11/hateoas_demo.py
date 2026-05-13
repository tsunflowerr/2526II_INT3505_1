# demos/hateoas.py
from flask import Blueprint, jsonify, url_for

hateoas_bp = Blueprint("hateoas", __name__, url_prefix="/hateoas")

products = {
    1: {"id": 1, "name": "Laptop", "price": 1500},
    2: {"id": 2, "name": "Mouse", "price": 20},
}


@hateoas_bp.get("/products")
def get_products():
    result = []

    for product in products.values():
        result.append({
            **product,
            "links": {
                "self": url_for("hateoas.get_product", product_id=product["id"], _external=True),
                "buy": url_for("hateoas.buy_product", product_id=product["id"], _external=True)
            }
        })

    return jsonify(result)


@hateoas_bp.get("/products/<int:product_id>")
def get_product(product_id):
    product = products.get(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        **product,
        "links": {
            "self": url_for("hateoas.get_product", product_id=product_id, _external=True),
            "all_products": url_for("hateoas.get_products", _external=True),
            "buy": url_for("hateoas.buy_product", product_id=product_id, _external=True)
        }
    })


@hateoas_bp.post("/products/<int:product_id>/buy")
def buy_product(product_id):
    product = products.get(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        "message": f"You bought {product['name']}",
        "links": {
            "product": url_for("hateoas.get_product", product_id=product_id, _external=True),
            "all_products": url_for("hateoas.get_products", _external=True)
        }
    })