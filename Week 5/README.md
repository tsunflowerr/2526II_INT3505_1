# So sánh lý thuyết các cách phân trang

Trong Week 5, có ba cách phân trang chính là `offset-limit`, `page-based` và `cursor-based`. Cả ba cách đều có cùng mục đích là chia dữ liệu thành nhiều phần nhỏ để API không phải trả toàn bộ dữ liệu trong một lần. Tuy nhiên, cách biểu diễn và cách sử dụng của chúng khác nhau.

`Offset-limit` là cách đơn giản nhất về mặt kỹ thuật. Client chỉ cần truyền vị trí bắt đầu và số lượng bản ghi cần lấy. Cách này dễ cài đặt và dễ hiểu với lập trình viên, nhưng hơi khó nhìn với người dùng cuối vì người dùng thường không nghĩ theo kiểu "bỏ qua bao nhiêu bản ghi". Khi dữ liệu lớn hoặc thay đổi liên tục, offset-limit cũng có thể làm kết quả giữa các lần gọi bị lệch.

`Page-based` là cách gần gũi hơn với người dùng vì nó dùng khái niệm số trang. Thay vì truyền vị trí bắt đầu, client truyền `page` và `page_size`. Về bản chất, page-based thường vẫn được đổi sang offset ở bên trong, nhưng cách dùng dễ hiểu hơn khi làm giao diện. Đây là kiểu phù hợp với các màn hình danh sách thông thường, ví dụ trang 1, trang 2, trang 3.

`Cursor-based` khác với hai cách trên vì nó không dựa vào số trang hay vị trí tuyệt đối. Thay vào đó, nó dùng một mốc dữ liệu cuối cùng đã đọc để lấy tiếp phần sau. Cách này phù hợp hơn khi dữ liệu lớn hoặc thay đổi thường xuyên vì kết quả thường ổn định hơn. Đổi lại, nó khó hiểu hơn lúc mới học và không thuận tiện nếu muốn nhảy ngay đến một trang bất kỳ.

Nếu so sánh ngắn gọn thì `offset-limit` dễ làm nhất, `page-based` dễ dùng nhất với người dùng cuối, còn `cursor-based` phù hợp hơn cho các hệ thống thực tế có dữ liệu lớn hoặc cập nhật liên tục. Trong thư mục này, phần giải thích cách từng kỹ thuật được áp dụng cụ thể đã được viết trực tiếp trong comment của các file code:

- `Offset_Limit_demo.py`
- `Page_based_demo.py`
- `Cursor_demo.py`
- `BTVN.py`
