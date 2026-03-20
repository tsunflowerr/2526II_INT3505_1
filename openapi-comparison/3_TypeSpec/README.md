# TypeSpec

File spec: `main.tsp`

TypeSpec là ngôn ngữ của Microsoft (2023), dùng cú pháp giống TypeScript. Có thể compile sang OpenAPI, JSON Schema, Protobuf.

## Cài đặt

```bash
npm install -g @typespec/compiler

# Cài dependencies của project
cd 3_TypeSpec
npm install
```

## Compile sang OpenAPI

```bash
# Compile TypeSpec sang OpenAPI YAML
npx tsp compile .

# File output: tsp-output/library-api.yaml
```

## Xem documentation

Sau khi compile, dùng file OpenAPI output để xem docs:
```bash
# Paste file tsp-output/library-api.yaml lên https://editor.swagger.io/
```

## Sinh code

Sau khi compile sang OpenAPI, dùng openapi-generator-cli:
```bash
# Compile trước
npx tsp compile .

# Sinh Python client từ file output
openapi-generator-cli generate -i tsp-output/library-api.yaml -g python -o generated/python-client
```

## Validate

```bash
# Kiểm tra lỗi cú pháp mà không sinh file output
npx tsp compile . --no-emit
```

## Tham khảo

- https://typespec.io/
- https://typespec.io/playground
- https://github.com/microsoft/typespec
