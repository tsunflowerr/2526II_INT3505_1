from flask import Flask, jsonify, request
import base64
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

# Cursor-based là kiểu phân trang theo mốc dữ liệu cuối cùng đã đọc.
# Ví dụ: /books?cursor=xxx&limit=5
# Trong file này cursor được tạo từ id cuối cùng rồi mã hóa base64.
# limit = số phần tử cần lấy tiếp.

def encode_cursor(id):
    """Mã hóa id thành cursor để client gửi lại ở lần gọi sau."""
    return base64.b64encode(str(id).encode()).decode()

def decode_cursor(cursor):
    """Giải mã cursor để lấy lại id gốc."""
    try:
        return int(base64.b64decode(cursor).decode())
    except:
        # Nếu cursor lỗi thì cho về 0 để bắt đầu lại từ đầu.
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
    # cursor là mốc cuối cùng của lần đọc trước.
    cursor = request.args.get("cursor", None)
    # limit là số phần tử muốn lấy tiếp.
    limit = int(request.args.get("limit", 5))

    # Mặc định bắt đầu từ đầu danh sách.
    start_idx = 0
    if cursor:
        # Giải mã cursor để lấy id cuối cùng.
        cursor_id = decode_cursor(cursor)
        # Tìm vị trí của id đó trong danh sách.
        for idx, book in enumerate(books):
            if book["id"] == cursor_id:
                # Bắt đầu từ phần tử ngay sau phần tử cuối cùng của trang trước.
                start_idx = idx + 1
                break

    # Lấy tiếp limit phần tử kể từ vị trí start_idx.
    result = books[start_idx: start_idx + limit]

    # Tạo cursor cho lần gọi tiếp theo.
    next_cursor = None
    if result and start_idx + limit < len(books):
        # Dùng id của phần tử cuối cùng trong result làm mốc mới.
        next_cursor = encode_cursor(result[-1]["id"])

    return jsonify({
        # Dữ liệu của lần gọi hiện tại.
        "data": result,
        # Cursor client vừa gửi lên.
        "cursor": cursor,
        # Cursor cho lần gọi kế tiếp.
        "next_cursor": next_cursor,
        "limit": limit,
        # Cho biết còn dữ liệu phía sau hay không.
        "has_next": next_cursor is not None
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
