from flask import Flask, jsonify, request
from flasgger import Swagger

# Tạo app Flask.
app = Flask(__name__)
# Bật Swagger để xem mô tả API.
swagger = Swagger(app)

# Dữ liệu mẫu để demo tìm kiếm và phân trang.
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
    """
    Search and paginate books
    ---
    tags:
      - Books
    responses:
      200:
        description: Paginated list of books
    """
    # Từ khóa tìm kiếm, chuyển về chữ thường để so sánh dễ hơn.
    search = request.args.get("search", "").lower()
    # Số trang hiện tại.
    page = int(request.args.get("page", 1))
    # Số phần tử trong mỗi trang.
    page_size = int(request.args.get("page_size", 5))

    # Lọc sách theo title hoặc author trước, sau đó mới phân trang.
    filtered = [b for b in books if search in b["title"].lower() or search in b["author"].lower()]

    # Tính vị trí bắt đầu của trang hiện tại.
    offset = (page - 1) * page_size
    # Lấy dữ liệu của trang hiện tại trên danh sách đã lọc.
    result = filtered[offset: offset + page_size]

    # Tính tổng số trang dựa trên số kết quả sau khi lọc.
    total_pages = (len(filtered) + page_size - 1) // page_size

    return jsonify({
        # Dữ liệu sau khi tìm kiếm và phân trang.
        "data": result,
        "search": search,
        "page": page,
        "page_size": page_size,
        # Tổng số kết quả tìm được.
        "total": len(filtered),
        "total_pages": total_pages,
        # Số phần tử thật sự trả về trong trang này.
        "count": len(result),
        # Có còn trang sau không.
        "has_next": page < total_pages,
        # Có còn trang trước không.
        "has_prev": page > 1
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
