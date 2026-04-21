from flask import Flask, jsonify, make_response

app = Flask(__name__)


@app.get("/api/v1/payments/info")
def payments_info_v1():
    response = make_response(jsonify({
        "message": "Payment API v1 is deprecated. Please move to /api/v2/payments/info"
    }))
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = "Wed, 31 Dec 2026 23:59:59 GMT"
    response.headers["Link"] = '</api/v2/payments/info>; rel="successor-version"'
    return response


@app.get("/api/v2/payments/info")
def payments_info_v2():
    return jsonify({
        "message": "Payment API v2 is active",
        "new_fields": ["paymentMethod", "currency"],
        "status": "recommended"
    })


if __name__ == "__main__":
    app.run(debug=True)
