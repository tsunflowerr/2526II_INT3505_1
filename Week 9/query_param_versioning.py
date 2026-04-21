from flask import Flask, jsonify, request

app = Flask(__name__)

orders = [
    {"id": 1, "total": 120},
    {"id": 2, "total": 250}
]

@app.get("/api/orders")
def get_orders():
    version = request.args.get("version", "1")

    if version == "2":
        data = []
        for o in orders:
            data.append({
                "order_id": o["id"],
                "amount": o["total"],
                "currency": "VND"
            })
        return jsonify(data)

    return jsonify(orders)

if __name__ == "__main__":
    app.run(debug=True)