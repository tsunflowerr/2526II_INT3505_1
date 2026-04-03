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

## Demo từng cái một

### 1) API Blueprint -> UI + Contract Testing

Mục tiêu: từ file `1_APIBlueprint/library-api.apib` sinh HTML đẹp bằng Aglio, sau đó dùng Dredd để test contract với server Flask.

#### Bước làm
1. Mở PowerShell và đi vào đúng folder dự án:
```powershell
Set-Location "E:\Code\Kiến trúc hướng dịch vụ\openapi-comparison"
```
2. Cài Flask cho server mẫu và cài công cụ demo:
```powershell
python -m pip install flask
npm install -g aglio dredd
```
3. Sinh giao diện tài liệu:
```powershell
Set-Location "E:\Code\Kiến trúc hướng dịch vụ\openapi-comparison\1_APIBlueprint"
aglio -i library-api.apib -o docs.html
```
4. Mở file docs bằng trình duyệt:
```powershell
Start-Process .\docs.html
```
5. Chạy Flask server mẫu ngay trong folder này:
```powershell
python .\server.py
```
6. Mở một terminal khác, quay lại folder API Blueprint rồi chạy Dredd:
```powershell
Set-Location "E:\Code\Kiến trúc hướng dịch vụ\openapi-comparison\1_APIBlueprint"
dredd library-api.apib http://localhost:5000
```

Lưu ý: Dredd chỉ pass nếu server trả đúng response như spec. Mình đã thêm file `1_APIBlueprint/server.py` để bạn chạy ngay.

### 2) RAML -> UI

Mục tiêu: từ file `2_RAML/library-api.raml` sinh HTML tài liệu bằng raml2html.

Mục tiêu phụ: chạy luôn server Flask để bạn gửi request thật lên API RAML.

#### Bước làm
1. Quay về folder gốc của repo:
```powershell
Set-Location "E:\Code\Kiến trúc hướng dịch vụ\openapi-comparison"
```
2. Cài Flask và công cụ RAML:
```powershell
python -m pip install flask
npm install -g raml2html
```
3. Chạy server RAML:
```powershell
Set-Location "E:\Code\Kiến trúc hướng dịch vụ\openapi-comparison\2_RAML"
python .\server.py
```
4. Sinh tài liệu HTML:
```powershell
Set-Location "E:\Code\Kiến trúc hướng dịch vụ\openapi-comparison\2_RAML"
raml2html library-api.raml > docs.html
```
5. Mở file docs:
```powershell
Start-Process .\docs.html
```
6. Mở terminal khác để gửi request thật:
```powershell
Invoke-RestMethod http://localhost:5000/books -Method GET
```
```powershell
$body = @{ title = "Designing Data-Intensive Applications"; author = "Martin Kleppmann"; isbn = "978-1449373320"; year = 2017; available = $true } | ConvertTo-Json
Invoke-RestMethod http://localhost:5000/books -Method POST -ContentType "application/json" -Body $body
```
```powershell
Invoke-RestMethod http://localhost:5000/books/1 -Method GET
```
```powershell
$body = @{ title = "Clean Code"; author = "Robert C. Martin"; isbn = "978-0132350884"; year = 2008; available = $false } | ConvertTo-Json
Invoke-RestMethod http://localhost:5000/books/1 -Method PUT -ContentType "application/json" -Body $body
```
```powershell
Invoke-RestMethod http://localhost:5000/books/1 -Method DELETE
```

### 3) TypeSpec -> OpenAPI Transformation

Mục tiêu: từ file `3_TypeSpec/main.tsp` biên dịch sang OpenAPI 3.0 để tận dụng hệ sinh thái OpenAPI.

Mục tiêu phụ: sinh luôn Python server từ file OpenAPI output rồi chạy thử request.

#### Bước làm
1. Quay về folder gốc của repo:
```powershell
Set-Location "E:\Code\Kiến trúc hướng dịch vụ\openapi-comparison"
```
2. Cài compiler TypeSpec:
```powershell
npm install -g @typespec/compiler
```
3. Cài dependencies của project:
```powershell
Set-Location "E:\Code\Kiến trúc hướng dịch vụ\openapi-comparison\3_TypeSpec"
npm install
```
4. Biên dịch TypeSpec sang OpenAPI:
```powershell
npx tsp compile .
```
5. File output sẽ nằm ở `tsp-output/library-api.yaml`.
6. Mở file OpenAPI sinh ra bằng Swagger UI:
```powershell
Start-Process "https://editor.swagger.io/"
```
Sau đó copy nội dung `tsp-output/library-api.yaml` dán vào Swagger Editor.

7. Sinh Python Flask server từ file OpenAPI output:
```powershell
Set-Location "E:\Code\Kiến trúc hướng dịch vụ\openapi-comparison\3_TypeSpec"
npm install -g @openapitools/openapi-generator-cli
openapi-generator-cli generate -i .\tsp-output\@typespec\openapi3\tsp-output\library-api.yaml -g python-flask -o .\generated\flask-server
```

8. Chạy server Python đã sinh:
```powershell
Set-Location "E:\Code\Kiến trúc hướng dịch vụ\openapi-comparison\3_TypeSpec\generated\flask-server"
python -m pip install -r requirements.txt
python -m openapi_server
```

9. Test request vào server vừa sinh:
```powershell
Invoke-RestMethod http://localhost:5000/books -Method GET
```

```powershell
$body = @{ title = "Clean Code"; author = "Robert C. Martin"; isbn = "978-0132350884"; year = 2008; available = $true } | ConvertTo-Json
Invoke-RestMethod http://localhost:5000/books -Method POST -ContentType "application/json" -Body $body
```

## Cách nói khi demo

- API Blueprint: nhấn mạnh “Markdown + Aglio + Dredd”.
- RAML: nhấn mạnh “YAML + raml2html + modular design”.
- TypeSpec: nhấn mạnh “TypeScript-like + compile sang OpenAPI 3.0”.
