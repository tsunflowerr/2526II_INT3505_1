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

@app.route('/demo', methods=['GET'])
def demo():
    """
    Demo components (schemas)
    ---
    summary: Demo components only

    responses:
      200:
        description: Return a book
        schema:
          $ref: '#/definitions/Book'

    definitions:
      Book:
        type: object
        required:
          - id
          - title
        properties:
          id:
            type: integer
          title:
            type: string
          author:
            type: string
    """
    return jsonify({
        "id": 1,
        "title": "Demo Book",
        "author": "Tester"
    })

@app.route('/demo2', methods=['GET'])
def demo2():
    """
    Demo reuse schema
    ---
    responses:
      200:
        description: Return another book
        schema:
          $ref: '#/definitions/Book'
    """
    return jsonify({
        "id": 2,
        "title": "Another Book",
        "author": "Tester"
    })

@app.route('/book', methods=['GET'])
def get_book():
    """
    Get a book
    ---
    summary: Demo schema

    responses:
      200:
        description: A book object
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            author:
              type: string
    """
    return jsonify({
        "id": 1,
        "title": "Clean Code",
        "author": "Robert"
    })


if __name__ == '__main__':
    app.run(debug=True)