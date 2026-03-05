# Phân tích mã lỗi HTTP 

**400 Bad Request**
Mã 400 nghĩa là server nhận được request nhưng dữ liệu gửi lên bị thiếu hoặc sai format. 

**404 Not Found**
Mã 404 là khi client yêu cầu một tài nguyên không tồn tại trên server. 

**429 Too Many Requests** là khi client gửi quá nhiều request trong một khoảng thời gian ngắn. Thường được trả về khi dùng rate-limit

**500 Internal Server Error** là lỗi phía server, xảy ra khi code bị crash hoặc có exception không được handle. Nếu database bị disconnect giữa chừng thì sẽ gặp lỗi này.

**401 Unauthorized** là khi client chưa xác thực (chưa đăng nhập).

**403 Forbidden** là khi client đã xác thực rồi nhưng không có quyền truy cập tài nguyên đó. Khác với 401 ở chỗ 401 là chưa đăng nhập còn 403 là đăng nhập rồi nhưng không đủ quyền.

**405 Method Not Allowed** là khi client gọi đúng URL nhưng sai method. Ví dụ gọi PATCH /users trong khi server chỉ định nghĩa GET và POST cho /users thì sẽ gặp lỗi này (Express mặc dịnh không trả 405 mà trả 404 cho trường hợp này).

**503 Service Unavailable** là khi server đang quá tải hoặc đang bảo trì, tạm thời không xử lý được request.