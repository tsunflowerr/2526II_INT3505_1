# API Blueprint

File spec: `library-api.apib`

API Blueprint dùng cú pháp Markdown để mô tả API. Dễ đọc, dễ viết, phù hợp khi ưu tiên documentation.

## Cài đặt

```bash
npm install -g dredd aglio
```

## Xem documentation

```bash
# Sinh file HTML documentation
aglio -i library-api.apib -o docs.html

# Mở file docs.html trong trình duyệt để xem
```

## Test tự động với Dredd

Dredd đọc file .apib, tự động sinh request, gọi vào server và kiểm tra response có đúng spec không.

```bash
# Cần có server đang chạy tại http://localhost:5000 trước
dredd library-api.apib http://localhost:5000
```

## Validate spec

```bash
# Dùng dredd để validate
dredd --dry-run library-api.apib http://localhost:5000
```

## Tham khảo

- https://apiblueprint.org/
- https://github.com/apiaryio/dredd
- https://github.com/danielgtaylor/aglio
