from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)

books = [
    {"id": 1, "title": "Clean Code", "author": "Robert"},
    {"id": 2, "title": "Design Patterns", "author": "GoF"}
]



@app.route('/books', methods=['GET'])
def get_books():
    """
    Get all books
    ---
    summary: Get all books
    parameters:
      - name: author
        in: query
        type: string
    responses:
      200:
        description: List of books
        schema:
          type: array
          items:
            $ref: '#/definitions/Book'
    """
    author = request.args.get('author')
    if author:
        return jsonify([b for b in books if b["author"] == author])
    return jsonify(books)


@app.route('/books', methods=['POST'])
def create_book():
    """
    Create a book
    ---
    summary: Create new book
    parameters:
      - in: body
        name: body
        schema:
          $ref: '#/definitions/Book'
    responses:
      201:
        description: Book created
    """
    data = request.json
    books.append(data)
    return jsonify(data), 201


@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    """
    Get book by ID
    ---
    summary: Get a book
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: A book
        schema:
          $ref: '#/definitions/Book'
      404:
        description: Not found
    """
    book = next((b for b in books if b["id"] == id), None)
    if not book:
        return {"error": "Not found"}, 404
    return jsonify(book)


@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    """
    Delete book
    ---
    summary: Delete a book
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      204:
        description: Deleted
    """
    global books
    books = [b for b in books if b["id"] != id]
    return '', 204



app.config['SWAGGER'] = {
    'title': 'Book API',
    'uiversion': 3
}

template = {
    "definitions": {
        "Book": {
            "type": "object",
            "required": ["id", "title"],
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "author": {"type": "string"}
            }
        }
    }
}

swagger = Swagger(app, template=template)


if __name__ == '__main__':
    app.run(debug=True)