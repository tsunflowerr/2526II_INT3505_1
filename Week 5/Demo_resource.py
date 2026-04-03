from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# /authors
# /authors/{id}
# /authors/{id}/books
# /books
# /books/{id}
# /books/{id}/reviews
# /users
# /users/{id}/borrowed-books

authors = [
    {"id": 1, "name": "Robert Martin"},
    {"id": 2, "name": "Martin Fowler"},
]

books = [
    {"id": 1, "title": "Clean Code", "author_id": 1},
    {"id": 2, "title": "Refactoring", "author_id": 2},
]


@app.route("/authors")
def get_authors():
    """
    Get all authors
    ---
    tags:
      - Authors
    responses:
      200:
        description: List of authors
    """
    return jsonify(authors)


@app.route("/authors/<int:author_id>")
def get_author(author_id):
    """
    Get author by id
    ---
    tags:
      - Authors
    responses:
      200:
        description: Author object or null if not found
    """
    author = next((a for a in authors if a["id"] == author_id), None)
    return jsonify(author)


@app.route("/authors/<int:author_id>/books")
def get_books_by_author(author_id):
    """
    Get books by author id
    ---
    tags:
      - Authors
      - Books
    responses:
      200:
        description: List of books by author
    """
    result = [b for b in books if b["author_id"] == author_id]
    return jsonify(result)


@app.route("/books")
def get_books():
    """
    Get all books
    ---
    tags:
      - Books
    responses:
      200:
        description: List of books
    """
    return jsonify(books)


if __name__ == "__main__":
    app.run(debug=True)
