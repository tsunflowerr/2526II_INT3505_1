# Outline Slides - So sánh 4 Format Tài liệu hóa API

## Slide 1: Giới thiệu
So sánh 4 format: OpenAPI, API Blueprint, RAML, TypeSpec

## Slide 2: API là gì?
Ứng dụng giao tiếp với nhau. Cách Frontend-Backend, App-Service liên lạc

## Slide 3: Tại sao cần tài liệu hóa?
Spec = contract rõ ràng. Frontend-Backend không phải đoán.

## Slide 4: 2 cách tài liệu hóa
Cũ: README, Word (không chuẩn, lạc hậu)
Mới: API Spec (chuẩn, sinh code tự động)

## Slide 5: 4 Format chính
1. OpenAPI (Phổ biến)
2. API Blueprint (Dễ đọc)
3. RAML (Modular)
4. TypeSpec (Mới)

## Slide 6: Demo API
Library Management API - 5 endpoints CRUD sách

## Slide 7: OpenAPI (2011 → 2016)
YAML/JSON - Phổ biến nhất - 50+ ngôn ngữ

## Slide 8: OpenAPI Example
library-api.yaml - Swagger UI, openapi-generator

## Slide 9: API Blueprint
Markdown - Dễ đọc - Ít tools

## Slide 10: API Blueprint Example
library-api.apib - Aglio, Dredd

## Slide 11: RAML
YAML - Traits, Types - Tốt API phức tạp

## Slide 12: RAML Example
library-api.raml - Modular, reusable

## Slide 13: TypeSpec (2023)
TypeScript-like - Type-safe - Microsoft

## Slide 14: TypeSpec Example
main.tsp - Compile → OpenAPI

## Slide 15: So sánh Cú pháp
OpenAPI (TB) | Blueprint (Dễ) | RAML (TB) | TypeSpec (Dễ)

## Slide 16: So sánh Phổ biến
OpenAPI (2011, Cao) | Blueprint (2013, Thấp) | RAML (2013, Vừa) | TypeSpec (2023, Tăng)

## Slide 17: So sánh Công cụ
OpenAPI: Swagger UI, 50+ generator
API Blueprint: Aglio, Dredd
RAML: API Console, Osprey
TypeSpec: Compile to OpenAPI

## Slide 18: Sinh code
Tất cả 4 đều sinh được - OpenAPI tốt nhất

## Slide 19: Lợi ích Specification
1. Single source of truth
2. Consistency
3. Parallel development
4. Auto documentation
5. Code generation

## Slide 20: API-First Workflow
Spec → Mock → Frontend test → Backend implement → SDK → Integration

## Slide 21: Chọn format khi nào?
OpenAPI: 95% projects
API Blueprint: Documentation priority
RAML: Complex API
TypeSpec: TypeScript team

## Slide 22: Best Practices
1. Version control spec
2. Spec is contract
3. Validate spec
4. Auto-generate in CI
5. Test early

## Slide 23: Tools Ecosystem
API Gateway (Kong, AWS) - Testing (Postman) - Docs (Swagger UI) - Code (openapi-generator)

## Slide 24: Kết luận
OpenAPI: Default choice
Blueprint: Dễ đọc
RAML: Modular
TypeSpec: Modern

Tất cả có: API design consistency, Parallel dev, Auto docs, Code gen, Better quality
