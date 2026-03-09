from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/users")
def get_users():
    # Nhất quán: Bọc dữ liệu trả về trong object "data"
    return {
        "data": [
            {"id": 1, "name": "Nguyễn Văn A"},
            {"id": 2, "name": "Trần Thị B"}
        ]
    }

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(name: str):
    if not name:
        # Xử lý lỗi nhất quán với mã 400 Bad Request
        raise HTTPException(status_code=400, detail="Tên không được để trống")
    return {
        "message": "Tạo người dùng thành công",
        "data": {"id": 3, "name": name}
    }