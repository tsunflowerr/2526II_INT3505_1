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

@app.route("/books")
def search_books():
    search = request.args.get("search", "").lower()
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 5))

    filtered = [b for b in books if search in b["title"].lower() or search in b["author"].lower()]

    offset = (page - 1) * page_size
    result = filtered[offset: offset + page_size]

    total_pages = (len(filtered) + page_size - 1) // page_size

    return jsonify({
        "data": result,
        "search": search,
        "page": page,
        "page_size": page_size,
        "total": len(filtered),
        "total_pages": total_pages,
        "count": len(result),
        "has_next": page < total_pages,
        "has_prev": page > 1
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
