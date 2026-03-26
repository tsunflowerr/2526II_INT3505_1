from flask import Flask, jsonify, request

app = Flask(__name__)

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

# Ý tưởng
# /books?offset=0&limit=10
# Logic
# offset = vị trí bắt đầu
# limit = số lượng record

@app.route("/books")
def books_offset():
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 5))

    result = books[offset: offset + limit]

    return jsonify({
        "data": result,
        "offset": offset,
        "limit": limit,
        "total": len(books),
        "count": len(result)
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)