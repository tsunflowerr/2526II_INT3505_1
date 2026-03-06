from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "OK", "message": "Server đang chạy!"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
