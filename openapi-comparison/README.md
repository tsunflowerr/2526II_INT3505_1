# So sánh 4 Format Tài liệu hoá API

So sánh OpenAPI, API Blueprint, RAML và TypeSpec qua cùng một API quản lý sách (Library Management).

## OpenAPI 3.0

Cú pháp YAML/JSON. Là format phổ biến nhất hiện nay, được hỗ trợ bởi rất nhiều công cụ như Swagger UI, Redoc, OpenAPI Generator. Có thể sinh code cho hơn 50 ngôn ngữ. Phù hợp với hầu hết mọi dự án.

File spec: `0_OpenAPI/library-api.yaml`

## API Blueprint

Cú pháp Markdown. Dễ đọc nhất trong 4 format, tập trung vào documentation hơn là sinh code. Công cụ hỗ trợ ít hơn OpenAPI (Dredd để test, Aglio để sinh docs). Phù hợp khi ưu tiên tài liệu dễ đọc.

File spec: `1_APIBlueprint/library-api.apib`

## RAML 1.0

Cú pháp YAML. Hỗ trợ traits, types và modularization tốt. Để sinh code thường phải convert sang OpenAPI trước. Phù hợp với API phức tạp cần chia module.

File spec: `2_RAML/library-api.raml`

## TypeSpec

Cú pháp giống TypeScript, do Microsoft phát triển (2023). Compile sang OpenAPI rồi dùng các công cụ của OpenAPI. Đang phát triển, phù hợp với team TypeScript hoặc hệ sinh thái Microsoft.

File spec: `3_TypeSpec/main.tsp`


