# RAML 1.0

File spec: `library-api.raml`

RAML (RESTful API Modeling Language) dùng cú pháp YAML. Hỗ trợ traits, types, modularization - phù hợp API phức tạp.

## Cài đặt

```bash
npm install -g raml2html
```

## Xem documentation

```bash
# Sinh file HTML từ RAML spec
raml2html library-api.raml > docs.html

# Mở file docs.html trong trình duyệt để xem
```

## Convert sang OpenAPI

RAML có thể convert sang OpenAPI để dùng các công cụ của OpenAPI:

```bash
npm install -g oas-raml-converter

# Convert RAML sang OpenAPI 2.0
oas-raml-converter --from RAML --to OAS20 library-api.raml > openapi.yaml
```

Sau khi convert, có thể dùng openapi-generator-cli để sinh code (xem folder 0_OpenAPI).

## Validate spec

```bash
# Dùng raml-parser để validate
npm install -g raml-1-parser
raml-validate library-api.raml
```

## Tham khảo

- https://raml.org/
- https://github.com/raml-org/raml-spec
- https://github.com/raml2html/raml2html
