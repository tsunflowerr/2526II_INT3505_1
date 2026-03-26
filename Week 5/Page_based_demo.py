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

# Ý tưởng: Page-based pagination
# /books?page=1&page_size=5
# Logic:
# page = số trang (bắt đầu từ 1)
# page_size = số record trên một trang

@app.route("/books")
def books_page():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 5))

    # Tính offset từ page và page_size
    offset = (page - 1) * page_size
    result = books[offset: offset + page_size]

    # Tính tổng số trang
    total_pages = (len(books) + page_size - 1) // page_size

    return jsonify({
        "data": result,
        "page": page,
        "page_size": page_size,
        "total": len(books),
        "total_pages": total_pages,
        "count": len(result),
        "has_next": page < total_pages,
        "has_prev": page > 1
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
