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

# Offset-limit là kiểu phân trang theo vị trí bắt đầu và số lượng cần lấy.
# Ví dụ: /books?offset=0&limit=10
# offset = bỏ qua bao nhiêu phần tử đầu tiên
# limit = lấy bao nhiêu phần tử tiếp theo

@app.route("/books")
def books_offset():
    """
    Offset-limit pagination for books
    ---
    tags:
      - Books
    responses:
      200:
        description: Offset-limit slice of books
    """
    # Nếu client không truyền offset thì mặc định bắt đầu từ đầu danh sách.
    offset = int(request.args.get("offset", 0))
    # Nếu client không truyền limit thì mặc định lấy 5 phần tử.
    limit = int(request.args.get("limit", 5))

    # Cắt list từ vị trí offset đến offset + limit.
    result = books[offset: offset + limit]

    return jsonify({
        # data là phần dữ liệu của lần gọi hiện tại.
        "data": result,
        # offset và limit được trả lại để client biết mình đang xem đoạn nào.
        "offset": offset,
        "limit": limit,
        # total là tổng số sách trong danh sách gốc.
        "total": len(books),
        # count là số phần tử thực tế trả về.
        "count": len(result)
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
