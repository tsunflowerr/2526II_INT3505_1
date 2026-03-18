from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/ping', methods=['GET'])
def ping():
    """
    Ping API
    ---
    summary: Simple path demo
    description: Đây là demo cho phần paths trong OpenAPI
    responses:
      200:
        description: OK
    """
    return jsonify({"message": "pong"})


if __name__ == '__main__':
    app.run(debug=True)