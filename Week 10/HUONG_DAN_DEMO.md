# Huong dan test demo Week 10

Thu muc `Week 10` gom 9 demo Flask doc lap ve API production, observability va security.

Moi file Python la mot Flask app rieng va mac dinh chay tren port `5000`. Khi demo file khac, hay tat server cu bang `Ctrl + C` roi chay file tiep theo.

## 1. Chuan bi moi truong

Mo PowerShell tai thu muc du an:

```powershell
cd "E:\Code\Kiến trúc hướng dịch vụ\Week 10"
```

Cai Flask neu may chua co:

```powershell
python -m pip install flask
```

Kiem tra Python:

```powershell
python --version
```

## 2. Cach chay chung

Chay mot demo:

```powershell
python .\01_production_api.py
```

Server se hien thi dang tuong tu:

```text
Running on http://127.0.0.1:5000
```

De test API, mo them mot cua so PowerShell khac va gui request bang `Invoke-RestMethod` hoac `Invoke-WebRequest`.

De tat server:

```text
Ctrl + C
```

Neu muon chay tren port khac:

```powershell
$env:PORT=5001
python .\01_production_api.py
```

Sau khi chay xong, co the xoa bien port trong cua so PowerShell hien tai:

```powershell
Remove-Item Env:\PORT
```

## 3. Demo 01 - Production API

File:

```text
01_production_api.py
```

Chay server:

```powershell
python .\01_production_api.py
```

Test health check:

```powershell
Invoke-RestMethod http://localhost:5000/health
```

Ket qua mong doi:

```json
{
  "env": "production",
  "status": "ok"
}
```

Test lay user theo id:

```powershell
Invoke-RestMethod http://localhost:5000/api/v1/users/1
```

Ket qua mong doi:

```json
{
  "id": 1,
  "name": "User 1",
  "version": "v1"
}
```

Test loi 404:

```powershell
Invoke-RestMethod http://localhost:5000/abc
```

Neu PowerShell bao loi do status `404`, co the dung:

```powershell
try {
  Invoke-RestMethod http://localhost:5000/abc
} catch {
  $_.ErrorDetails.Message
}
```

Y can trinh bay:

- API co endpoint `/health` de kiem tra service con song.
- Endpoint API duoc version theo `/api/v1/...`.
- Loi `404` tra ve JSON thay vi HTML mac dinh.
- Co the cau hinh `ENV_NAME`, `API_VERSION`, `PORT` bang bien moi truong.

## 4. Demo 02 - Structured JSON Logging

File:

```text
02_structured_json_logging.py
```

Chay server:

```powershell
python .\02_structured_json_logging.py
```

Gui request co `X-Request-ID`:

```powershell
Invoke-RestMethod http://localhost:5000/api/v1/orders/101 -Headers @{"X-Request-ID"="demo-req-001"}
```

Ket qua mong doi:

```json
{
  "currency": "VND",
  "id": 101,
  "total": 199000
}
```

Quan sat terminal dang chay Flask. Se co log dang JSON, vi du:

```json
{"level": "INFO", "message": "order_viewed", "request_id": "demo-req-001", "order_id": 101}
{"level": "INFO", "message": "request_completed", "request_id": "demo-req-001", "method": "GET", "path": "/api/v1/orders/101", "status_code": 200}
```

Kiem tra response header `X-Request-ID`:

```powershell
(Invoke-WebRequest http://localhost:5000/api/v1/orders/101 -Headers @{"X-Request-ID"="demo-req-002"}).Headers
```

Y can trinh bay:

- Log khong chi la chuoi text, ma la JSON co cau truc.
- Moi request co `request_id` de truy vet.
- Log co method, path, status code, duration va IP client.
- Dang log nay phu hop voi ELK, Loki, Datadog, CloudWatch.

## 5. Demo 03 - Metrics Prometheus

File:

```text
03_metrics_prometheus.py
```

Chay server:

```powershell
python .\03_metrics_prometheus.py
```

Goi API nhieu lan:

```powershell
Invoke-RestMethod http://localhost:5000/api/v1/products
Invoke-RestMethod http://localhost:5000/api/v1/products
Invoke-RestMethod http://localhost:5000/api/v1/products
```

Xem metrics:

```powershell
Invoke-RestMethod http://localhost:5000/metrics
```

Ket qua mong doi co dang:

```text
# HELP flask_http_requests_total Total HTTP requests
# TYPE flask_http_requests_total counter
flask_http_requests_total{method="GET",path="/api/v1/products",status="200"} 3
# HELP flask_http_request_duration_seconds_avg Average request latency
# TYPE flask_http_request_duration_seconds_avg gauge
flask_http_request_duration_seconds_avg{path="/api/v1/products"} 0.05
```

Y can trinh bay:

- `/metrics` la endpoint cho he thong monitoring doc.
- Counter dem tong so request theo method, path va status.
- Gauge hien thi latency trung binh.
- Prometheus co the scrape endpoint nay de ve dashboard tren Grafana.

## 6. Demo 04 - Simple Tracing

File:

```text
04_simple_tracing.py
```

Chay server:

```powershell
python .\04_simple_tracing.py
```

Gui request co trace id:

```powershell
Invoke-RestMethod http://localhost:5000/api/v1/service-info -Headers @{"X-Trace-ID"="trace-demo-001"}
```

Ket qua mong doi:

```json
{
  "id": 1,
  "name": "Inventory service"
}
```

Quan sat terminal dang chay Flask. Se thay trace gom `trace_id`, danh sach `spans` va `status_code`.

Kiem tra response header:

```powershell
(Invoke-WebRequest http://localhost:5000/api/v1/service-info -Headers @{"X-Trace-ID"="trace-demo-002"}).Headers
```

Y can trinh bay:

- Tracing cho biet mot request di qua nhung buoc nao.
- `trace_id` giup lien ket log cua cung mot request.
- `span` dai dien cho mot cong viec nho, vi du HTTP request hoac database query.
- Moi span co thoi gian xu ly rieng.

## 7. Demo 05 - Rate Limiting

File:

```text
05_rate_limiting.py
```

Chay server:

```powershell
python .\05_rate_limiting.py
```

Gui 5 request hop le:

```powershell
1..5 | ForEach-Object {
  Invoke-RestMethod http://localhost:5000/api/v1/payments -Headers @{"X-API-Key"="student-demo"}
}
```

Gui request thu 6:

```powershell
try {
  Invoke-RestMethod http://localhost:5000/api/v1/payments -Headers @{"X-API-Key"="student-demo"}
} catch {
  $_.ErrorDetails.Message
}
```

Ket qua mong doi:

```json
{
  "error": "rate_limit_exceeded",
  "retry_after_seconds": 59
}
```

Test voi API key khac:

```powershell
Invoke-RestMethod http://localhost:5000/api/v1/payments -Headers @{"X-API-Key"="student-demo-2"}
```

Y can trinh bay:

- Moi client duoc dinh danh bang `X-API-Key` hoac IP.
- Gioi han mac dinh la 5 request trong 60 giay.
- Khi vuot gioi han, API tra ve HTTP `429`.
- Rate limiting giup bao ve API truoc spam, bot hoac client goi qua nhieu.

## 8. Demo 06 - Circuit Breaker

File:

```text
06_circuit_breaker.py
```

Chay server:

```powershell
python .\06_circuit_breaker.py
```

Goi API nhieu lan:

```powershell
1..10 | ForEach-Object {
  try {
    Invoke-RestMethod http://localhost:5000/api/v1/payment-provider-status
  } catch {
    $_.ErrorDetails.Message
  }
}
```

Ket qua co the thay:

```json
{
  "error": "payment_gateway_failed",
  "circuit_state": "closed"
}
```

Sau khi loi lien tiep du nguong:

```json
{
  "error": "circuit_open",
  "circuit_state": "open"
}
```

Cho khoang 10 giay roi goi lai:

```powershell
Start-Sleep -Seconds 10
Invoke-RestMethod http://localhost:5000/api/v1/payment-provider-status
```

Y can trinh bay:

- Demo gia lap payment gateway bi loi ngau nhien 70%.
- Sau 3 lan loi, circuit breaker chuyen sang `open`.
- Khi `open`, API khong tiep tuc goi provider dang loi ma tra loi nhanh.
- Sau thoi gian recovery, circuit co the thu lai o trang thai `half_open`.

## 9. Demo 07 - Security Headers va WAF

File:

```text
07_security_headers_and_waf.py
```

Chay server:

```powershell
python .\07_security_headers_and_waf.py
```

Request binh thuong:

```powershell
Invoke-RestMethod "http://localhost:5000/api/v1/search?q=laptop"
```

Ket qua mong doi:

```json
{
  "query": "laptop",
  "results": []
}
```

Kiem tra security headers:

```powershell
(Invoke-WebRequest "http://localhost:5000/api/v1/search?q=laptop").Headers
```

Can thay cac header:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: no-referrer
Content-Security-Policy: default-src 'none'; frame-ancestors 'none'
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

Test WAF chan XSS:

```powershell
try {
  Invoke-RestMethod "http://localhost:5000/api/v1/search?q=<script>alert(1)</script>"
} catch {
  $_.ErrorDetails.Message
}
```

Test WAF chan SQL injection:

```powershell
try {
  Invoke-RestMethod "http://localhost:5000/api/v1/search?q=union select password from users"
} catch {
  $_.ErrorDetails.Message
}
```

Test WAF chan path traversal:

```powershell
try {
  Invoke-RestMethod "http://localhost:5000/api/v1/search?q=../etc/passwd"
} catch {
  $_.ErrorDetails.Message
}
```

Ket qua bi chan:

```json
{
  "error": "blocked_by_waf"
}
```

Y can trinh bay:

- Security headers giup giam rui ro clickjacking, MIME sniffing va leak referrer.
- WAF don gian kiem tra query string va body.
- Cac pattern nguy hiem nhu `<script>`, `union select`, `drop table`, `../` se bi chan.
- Khi bi chan, API tra HTTP `403`.

## 10. Demo 08 - Audit Logs

File:

```text
08_audit_logs.py
```

Chay server:

```powershell
python .\08_audit_logs.py
```

Xoa file audit cu neu muon demo sach:

```powershell
Remove-Item .\audit.log -ErrorAction SilentlyContinue
```

Gui request demo audit:

```powershell
Invoke-RestMethod http://localhost:5000/api/v1/audit-demo -Headers @{"X-User-ID"="admin01"; "X-Request-ID"="audit-req-001"}
```

Lock user:

```powershell
Invoke-RestMethod -Method Post http://localhost:5000/api/v1/admin/users/5/lock -Headers @{"X-User-ID"="admin01"; "X-Request-ID"="audit-req-002"}
```

Doc file audit:

```powershell
Get-Content .\audit.log
```

Ket qua audit co dang:

```json
{"time": "2026-05-15T00:00:00Z", "request_id": "audit-req-001", "actor": "admin01", "action": "view_audit_demo", "resource": "audit-demo", "status": "success", "ip": "127.0.0.1"}
{"time": "2026-05-15T00:00:01Z", "request_id": "audit-req-002", "actor": "admin01", "action": "lock_user", "resource": "user:5", "status": "success", "ip": "127.0.0.1"}
```

Y can trinh bay:

- Audit log ghi lai hanh dong quan trong trong he thong.
- Moi event gom thoi gian, request id, actor, action, resource, status va IP.
- Audit log khac voi application log: audit tap trung vao ai da lam gi.
- Cac thao tac admin, bao mat, thanh toan nen co audit log.

## 11. Demo 09 - Full Observability Security API

File:

```text
09_full_observability_security_api.py
```

Day la demo tong hop: health check, structured logging, metrics, audit log, WAF, security headers va rate limiting.

Chay server:

```powershell
python .\09_full_observability_security_api.py
```

Xoa audit cu neu muon demo sach:

```powershell
Remove-Item .\audit.log -ErrorAction SilentlyContinue
```

Test health:

```powershell
Invoke-RestMethod http://localhost:5000/health
```

Test invoice API:

```powershell
Invoke-RestMethod http://localhost:5000/api/v1/invoices/10 -Headers @{"X-User-ID"="user01"; "X-Request-ID"="req-full-demo"}
```

Ket qua mong doi:

```json
{
  "amount": 450000,
  "currency": "VND",
  "id": 10
}
```

Quan sat terminal de thay structured log `request_completed`.

Doc audit log:

```powershell
Get-Content .\audit.log
```

Xem metrics:

```powershell
Invoke-RestMethod http://localhost:5000/metrics
```

Kiem tra security headers:

```powershell
(Invoke-WebRequest http://localhost:5000/api/v1/invoices/10).Headers
```

Test WAF:

```powershell
try {
  Invoke-RestMethod "http://localhost:5000/api/v1/invoices/10?q=<script>"
} catch {
  $_.ErrorDetails.Message
}
```

Test rate limit:

```powershell
1..12 | ForEach-Object {
  try {
    Invoke-RestMethod http://localhost:5000/api/v1/invoices/10 -Headers @{"X-API-Key"="demo-full"; "X-User-ID"="user01"}
  } catch {
    $_.ErrorDetails.Message
  }
}
```

Ket qua mong doi sau khi vuot gioi han:

```json
{
  "error": "rate_limit_exceeded"
}
```

Y can trinh bay:

- Day la API production mini gom nhieu lop bao ve va quan sat.
- Observability gom log, metrics va audit.
- Security gom WAF, security headers va rate limiting.
- `X-Request-ID` giup truy vet request tu response, log va audit.
- `/metrics` giup monitoring, `/health` giup health check.

## 12. Thu tu demo de trinh bay tren lop

Nen demo theo thu tu:

1. `01_production_api.py`: API production co ban.
2. `02_structured_json_logging.py`: log co cau truc.
3. `03_metrics_prometheus.py`: metrics cho monitoring.
4. `04_simple_tracing.py`: trace request.
5. `05_rate_limiting.py`: gioi han request.
6. `06_circuit_breaker.py`: chong loi lan truyen khi service phu thuoc bi loi.
7. `07_security_headers_and_waf.py`: bao mat header va chan payload nguy hiem.
8. `08_audit_logs.py`: ghi vet hanh dong quan trong.
9. `09_full_observability_security_api.py`: tong hop cac ky thuat.

## 13. Loi thuong gap

### Port 5000 dang duoc dung

Neu bao loi port dang duoc dung, tat server cu bang `Ctrl + C`.

Hoac chay file moi tren port khac:

```powershell
$env:PORT=5001
python .\09_full_observability_security_api.py
```

Test lai bang:

```powershell
Invoke-RestMethod http://localhost:5001/health
```

### PowerShell hien loi khi API tra 403, 404, 429, 503

`Invoke-RestMethod` se coi HTTP error la exception. Dung mau sau de xem body:

```powershell
try {
  Invoke-RestMethod http://localhost:5000/some-error-endpoint
} catch {
  $_.ErrorDetails.Message
}
```

### Khong co module Flask

Cai lai Flask:

```powershell
python -m pip install flask
```

Neu may co nhieu ban Python, thu:

```powershell
py -m pip install flask
py .\01_production_api.py
```

### File audit.log co du lieu cu

Xoa file audit truoc khi demo:

```powershell
Remove-Item .\audit.log -ErrorAction SilentlyContinue
```

## 14. Script demo nhanh cho file 09

Chay server:

```powershell
python .\09_full_observability_security_api.py
```

Mo PowerShell khac va chay:

```powershell
Invoke-RestMethod http://localhost:5000/health
Invoke-RestMethod http://localhost:5000/api/v1/invoices/10 -Headers @{"X-User-ID"="user01"; "X-Request-ID"="req-demo-09"}
Invoke-RestMethod http://localhost:5000/metrics
Get-Content .\audit.log
(Invoke-WebRequest http://localhost:5000/api/v1/invoices/10).Headers
try {
  Invoke-RestMethod "http://localhost:5000/api/v1/invoices/10?q=<script>"
} catch {
  $_.ErrorDetails.Message
}
```

Ket luan khi demo:

```text
Week 10 minh hoa cac yeu to can co cua API production: health check, logging, metrics, tracing, rate limiting, circuit breaker, security headers, WAF va audit log. File 09 gom cac ky thuat chinh vao mot API tong hop.
```
