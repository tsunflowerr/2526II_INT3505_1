from flask import Flask, jsonify

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Mouse"}
]

@app.get("/api/v1/products")
def products_v1():
    return jsonify(products)

@app.get("/api/v2/products")
def products_v2():
    data = []
    for p in products:
        data.append({
            "id": p["id"],
            "title": p["name"],
            "in_stock": True
        })
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)