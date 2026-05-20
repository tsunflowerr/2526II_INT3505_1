from flask import Flask, request, jsonify

app = Flask(__name__)

real_orders = []
sandbox_orders = []

@app.route("/")
def home():
    return """
    <h1>Payment API Sandbox Demo</h1>
    <p>POST /api/orders?mode=sandbox để test.</p>
    <p>POST /api/orders?mode=live để tạo đơn thật.</p>
    """

@app.route("/api/orders", methods=["POST"])
def create_order():
    mode = request.args.get("mode", "sandbox")
    data = request.json

    order = {
        "id": len(sandbox_orders if mode == "sandbox" else real_orders) + 1,
        "product": data.get("product"),
        "amount": data.get("amount"),
        "mode": mode
    }

    if mode == "sandbox":
        sandbox_orders.append(order)
        return jsonify({
            "message": "Sandbox order created. No real payment happened.",
            "order": order
        })

    if mode == "live":
        real_orders.append(order)
        return jsonify({
            "message": "Live order created.",
            "order": order
        })

    return jsonify({"error": "mode must be sandbox or live"}), 400

@app.route("/api/orders")
def list_orders():
    return jsonify({
        "sandbox_orders": sandbox_orders,
        "real_orders": real_orders
    })

if __name__ == "__main__":
    app.run(debug=True)
