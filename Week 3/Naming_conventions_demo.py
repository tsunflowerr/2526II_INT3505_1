from flask import Flask, jsonify

app = Flask(__name__)

# /user  ❌ không khuyến khích
@app.route("/api/v1/users")
def get_users():
    return jsonify([
        {"id": 1, "name": "An"},
        {"id": 2, "name": "Binh"}
    ])

# /Products      ❌
# /PRODUCTS      ❌
@app.route("/api/v1/products")
def get_products():
    return jsonify([
        {"id": 1, "name": "Laptop"},
        {"id": 2, "name": "Keyboard"}
    ])


#/orderItems    ❌ 
#/order_items   ❌ 
@app.route("/api/v1/order-items")
def get_order_items():
    return jsonify([
        {"id": 101, "product": "Laptop"},
        {"id": 102, "product": "Mouse"}
    ])



if __name__ == "__main__":
    app.run(debug=True)