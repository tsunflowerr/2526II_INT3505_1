from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Data Model Library
# User
#  - id
#  - name
#  - email

# Book
#  - id
#  - title
#  - author
#  - available

# Borrow
#  - id
#  - user_id
#  - book_id
#  - borrow_date

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

borrows = [
    {"id": 1, "user_id": 1, "book_id": 2}
]

@app.route("/users/<int:user_id>/borrowed-books")
def borrowed_books(user_id):
    """
    Get borrowed books entries for a user
    ---
    tags:
      - Users
      - Borrows
    responses:
      200:
        description: Borrow records of the user
    """
    borrowed = [b for b in borrows if b["user_id"] == user_id]
    return jsonify(borrowed)


if __name__ == "__main__":
    app.run(debug=True, port=5000)