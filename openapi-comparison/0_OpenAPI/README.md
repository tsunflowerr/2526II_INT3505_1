# OpenAPI 3.0

File spec: `library-api.yaml`

OpenAPI (trước đây là Swagger) là format phổ biến nhất để mô tả RESTful API. Dùng cú pháp YAML hoặc JSON.

## Cài đặt

```bash
npm install -g @openapitools/openapi-generator-cli
```

## Xem documentation

Cách 1: Paste nội dung file `library-api.yaml` lên https://editor.swagger.io/

Cách 2: Dùng Swagger UI trên máy
```bash
npx @redocly/cli preview-docs library-api.yaml
```

## Sinh code

```bash
# Sinh Python client
openapi-generator-cli generate -i library-api.yaml -g python -o generated/python-client

# Sinh Flask server
openapi-generator-cli generate -i library-api.yaml -g python-flask -o generated/flask-server

# Sinh Java client
openapi-generator-cli generate -i library-api.yaml -g java -o generated/java-client
```

Xem danh sách ngôn ngữ hỗ trợ:
```bash
openapi-generator-cli list
```

## Validate spec

```bash
openapi-generator-cli validate -i library-api.yaml
```

## Tham khảo

- https://swagger.io/specification/
- https://editor.swagger.io/
- https://openapi-generator.tech/
