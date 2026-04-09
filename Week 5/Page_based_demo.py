from flask import Flask, jsonify, request
from flasgger import Swagger

# Tạo app Flask.
app = Flask(__name__)
# Bật Swagger để xem mô tả API.
swagger = Swagger(app)

# Dữ liệu mẫu để demo phân trang.
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

# Page-based là kiểu phân trang theo số trang.
# Ví dụ: /books?page=1&page_size=5
# page = trang hiện tại, bắt đầu từ 1
# page_size = số phần tử trong mỗi trang

@app.route("/books")
def books_page():
    """
    Page-based pagination for books
    ---
    tags:
      - Books
    responses:
      200:
        description: Page of books with pagination metadata
    """
    # Nếu không truyền page thì mặc định lấy trang đầu tiên.
    page = int(request.args.get("page", 1))
    # Nếu không truyền page_size thì mặc định mỗi trang có 5 phần tử.
    page_size = int(request.args.get("page_size", 5))

    # Đổi từ page sang offset để cắt dữ liệu.
    offset = (page - 1) * page_size
    # Lấy dữ liệu của trang hiện tại.
    result = books[offset: offset + page_size]

    # Tính tổng số trang từ tổng số phần tử và page_size.
    total_pages = (len(books) + page_size - 1) // page_size

    return jsonify({
        # Dữ liệu của trang hiện tại.
        "data": result,
        "page": page,
        "page_size": page_size,
        # Tổng số phần tử của toàn bộ danh sách.
        "total": len(books),
        # Tổng số trang.
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
