from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "978-0132350884",
        "year": 2008,
        "available": True,
    }
]


@app.route("/books", methods=["GET"])
def list_books():
    return jsonify(books)


@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json(silent=True) or {}
    new_book = {
        "id": len(books) + 1,
        "title": data.get("title", "Unknown"),
        "author": data.get("author", "Unknown"),
        "isbn": data.get("isbn", ""),
        "year": data.get("year", 0),
        "available": data.get("available", True),
    }
    books.append(new_book)
    return jsonify(new_book), 201


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((item for item in books if item["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = next((item for item in books if item["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json(silent=True) or {}
    book.update(
        {
            "title": data.get("title", book["title"]),
            "author": data.get("author", book["author"]),
            "isbn": data.get("isbn", book["isbn"]),
            "year": data.get("year", book["year"]),
            "available": data.get("available", book["available"]),
        }
    )
    return jsonify(book)


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    index = next((i for i, item in enumerate(books) if item["id"] == book_id), None)
    if index is None:
        return jsonify({"error": "Book not found"}), 404

    books.pop(index)
    return "", 204


if __name__ == "__main__":
    app.run(port=5000, debug=True)