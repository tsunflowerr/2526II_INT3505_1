import os

from flask import Flask, jsonify, request
from pymongo import MongoClient


app = Flask(__name__)


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "week7_demo")
MONGO_COLLECTION = "products"


def get_collection():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return client, db[MONGO_COLLECTION]


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/products")
def get_products():
    client, products = get_collection()
    data = list(products.find({}, {"_id": 1, "name": 1, "price": 1}))
    client.close()
    return jsonify(data), 200


@app.get("/products/<product_id>")
def get_product(product_id):
    client, products = get_collection()
    product = products.find_one({"_id": product_id}, {"_id": 1, "name": 1, "price": 1})
    client.close()
    if not product:
        return jsonify({"message": "Khong tim thay product"}), 404
    return jsonify(product), 200


@app.post("/products")
def create_product():
    data = request.get_json(silent=True) or {}
    if "_id" not in data or "name" not in data or "price" not in data:
        return jsonify({"message": "Can _id, name, price"}), 400

    client, products = get_collection()
    product = {
        "_id": data["_id"],
        "name": data["name"],
        "price": data["price"],
    }
    products.insert_one(product)
    client.close()
    return jsonify(product), 201


@app.put("/products/<product_id>")
def update_product(product_id):
    data = request.get_json(silent=True) or {}
    client, products = get_collection()
    result = products.update_one({"_id": product_id}, {"$set": data})
    if result.matched_count == 0:
        client.close()
        return jsonify({"message": "Khong tim thay product"}), 404

    product = products.find_one({"_id": product_id}, {"_id": 1, "name": 1, "price": 1})
    client.close()
    return jsonify(product), 200


@app.delete("/products/<product_id>")
def delete_product(product_id):
    client, products = get_collection()
    result = products.delete_one({"_id": product_id})
    client.close()
    if result.deleted_count == 0:
        return jsonify({"message": "Khong tim thay product"}), 404
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
