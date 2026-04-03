from flask import Flask, jsonify, request
import base64
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Sample data
books = [
    {"id": 1, "title": "Python 101", "author": "John Doe"},
    {"id": 2, "title": "Flask Guide", "author": "Jane Smith"},
    {"id": 3, "title": "REST API Design", "author": "Bob Johnson"},
    {"id": 4, "title": "Microservices", "author": "Alice Brown"},
    {"id": 5, "title": "Docker Mastery", "author": "Charlie Wilson"},
    {"id": 6, "title": "Kubernetes Pro", "author": "Diana Lee"},
    {"id": 7, "title": "GraphQL Basics", "author": "Eve Martinez"},
    {"id": 8, "title": "Database Design", "author": "Frank Garcia"},
]

# Ý tưởng: Cursor-based pagination
# /books?cursor=xxx&limit=5
# Logic:
# cursor = base64(id) của phần tử cuối cùng
# limit = số lượng record

def encode_cursor(id):
    """Encode id thành cursor"""
    return base64.b64encode(str(id).encode()).decode()

def decode_cursor(cursor):
    """Decode cursor thành id"""
    try:
        return int(base64.b64decode(cursor).decode())
    except:
        return 0

@app.route("/books")
def books_cursor():
    """
    Cursor-based pagination for books
    ---
    tags:
      - Books
    responses:
      200:
        description: Page of books with next cursor
    """
    cursor = request.args.get("cursor", None)
    limit = int(request.args.get("limit", 5))

    # Nếu có cursor, tìm vị trí bắt đầu
    start_idx = 0
    if cursor:
        cursor_id = decode_cursor(cursor)
        # Tìm vị trí của cursor_id trong list
        for idx, book in enumerate(books):
            if book["id"] == cursor_id:
                start_idx = idx + 1
                break

    result = books[start_idx: start_idx + limit]

    # Tính next_cursor
    next_cursor = None
    if result and start_idx + limit < len(books):
        next_cursor = encode_cursor(result[-1]["id"])

    return jsonify({
        "data": result,
        "cursor": cursor,
        "next_cursor": next_cursor,
        "limit": limit,
        "has_next": next_cursor is not None
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
