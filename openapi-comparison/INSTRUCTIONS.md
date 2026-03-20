# Hướng dẫn - So sánh 4 Format Tài liệu hóa API

## Mục đích

So sánh 4 định dạng standard để tài liệu hóa API:
- OpenAPI (Phổ biến nhất, tools nhiều)
- API Blueprint (Dễ đọc, Markdown-based)
- RAML (Modular, traits và types)
- TypeSpec (Mới, Microsoft, type-safe)

Mục tiêu: Hiểu ưu/nhược điểm mỗi format, khi nào dùng cái gì.

## Yêu cầu

### Bắt buộc
- Python 3.7+
- pip (Python package manager)
- requests library: `pip install requests`

### Tùy chọn (cho xem documentation, generate code)
- Node.js v14+
- npm

## Phương pháp so sánh

### 1. So sánh theo cú pháp
- YAML vs Markdown vs TypeScript-like
- Dễ đọc, dễ viết, complexity

### 2. So sánh theo ecosystem
- Tools hỗ trợ
- Community size
- Enterprise adoption

### 3. So sánh theo khả năng sinh code
- Có thể sinh server/client code không?
- Bao nhiêu ngôn ngữ support?

### 4. So sánh theo use cases
- OpenAPI: 95% cases (default)
- API Blueprint: Documentation priority
- RAML: Complex API, modularization
- TypeSpec: TypeScript teams, Microsoft ecosystem

## Dàn ý chung

Tất cả 4 format:
1. Định nghĩa cùng API (Library Management - CRUD sách)
2. Có thể xem spec file để so sánh cú pháp
3. Có thể validate, generate docs, generate code
4. Có test_generated.py demo để kiểm tra functionality

Mỗi format khác nhau về:
- Dễ đọc
- Tools support
- Code generation
- Community adoption
