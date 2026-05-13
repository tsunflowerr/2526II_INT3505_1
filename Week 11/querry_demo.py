# demos/query.py
from flask import Blueprint, jsonify, request

query_bp = Blueprint("query", __name__, url_prefix="/query")

products = [
    {"id": 1, "name": "Python Book", "category": "book", "price": 120},
    {"id": 2, "name": "Flask Book", "category": "book", "price": 90},
    {"id": 3, "name": "Keyboard", "category": "device", "price": 300},
    {"id": 4, "name": "Mouse", "category": "device", "price": 80},
]


@query_bp.get("/products")
def search_products():
    category = request.args.get("category")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    keyword = request.args.get("keyword", "").lower()

    result = products

    if category:
        result = [
            product for product in result
            if product["category"] == category
        ]

    if min_price is not None:
        result = [
            product for product in result
            if product["price"] >= min_price
        ]

    if max_price is not None:
        result = [
            product for product in result
            if product["price"] <= max_price
        ]

    if keyword:
        result = [
            product for product in result
            if keyword in product["name"].lower()
        ]

    return jsonify({
        "filters": {
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "keyword": keyword
        },
        "total": len(result),
        "data": result
    })