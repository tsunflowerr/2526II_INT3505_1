# Week 7 - Huong dan chay chi tiet

Tai lieu nay huong dan cach chay tung file trong thu muc `Week 7`.

## 1. Noi dung thu muc

### File Python co the chay truc tiep

- `mini_user_api.py`: API Flask nho, khong can MongoDB
- `mongo_demo.py`: demo ket noi MongoDB bang `pymongo`
- `mongo_schema_model_demo.py`: demo schema/model bang `mongoengine`
- `api_db_mapping_demo.py`: demo mapping giua JSON API va document MongoDB
- `validation_error_demo.py`: demo validation va xu ly loi
- `product_crud_api.py`: API CRUD Product voi Flask + MongoDB

### File ho tro

- `start_mongodb.ps1`: bat MongoDB local bang binary da dinh kem
- `stop_mongodb.ps1`: tat MongoDB local
- `.env.example`: mau bien moi truong
- `user-api-openapi.yaml`: file mo ta OpenAPI ban rut gon
- `user-api-openapi-full.yaml`: file mo ta OpenAPI day du

### Thu muc du lieu

- `mongodb/`: noi luu data va log MongoDB
- `mongodb-extract/`: chua binary `mongod.exe`

## 2. Dieu kien can truoc khi chay

Can co:

- Python 3 da cai san
- `pip`
- PowerShell

Kiem tra nhanh:

```powershell
python --version
pip --version
```

## 3. Cai thu vien

Chay trong thu muc `Week 7`:

```powershell
pip install flask pymongo python-dotenv mongoengine
```

Neu muon tach moi truong ao:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install flask pymongo python-dotenv mongoengine
```

## 4. Tao file `.env`

Tao file `.env` tu file mau:

```powershell
Copy-Item .env.example .env
```

Noi dung mac dinh:

```env
MONGO_URI=mongodb://localhost:27017/
MONGO_DB=week7_demo
MONGO_COLLECTION=users
```

## 5. Chay MongoDB local

### Cach 1: dung script co san

```powershell
.\start_mongodb.ps1
```

Neu tat:

```powershell
.\stop_mongodb.ps1
```

### Kiem tra MongoDB da len chua

```powershell
netstat -ano | findstr :27017
```

Neu thay port `27017` dang `LISTENING` thi MongoDB da chay.

## 6. Luu y quan trong ve MongoDB trong thu muc nay

Trong moi truong hien tai, minh da kiem tra thuc te va gap loi khi chay `mongod.exe`:

- `localhost:27017` khong bind thanh cong
- log co cac dong dang `Access is denied`
- WiredTiger fail khi rename/remove file nhu `WiredTiger.turtle` hoac `WiredTigerPreplog...`

Neu ban gap tinh trang nay, cac file duoi day se loi ket noi DB:

- `mongo_demo.py`
- `mongo_schema_model_demo.py`
- `api_db_mapping_demo.py`
- `validation_error_demo.py`
- `product_crud_api.py` voi cac endpoint `/products`

### Cach xu ly thuong dung

Thu lan luot:

1. Tat toan bo `mongod` dang chay:

```powershell
Get-Process mongod -ErrorAction SilentlyContinue | Stop-Process -Force
```

2. Mo PowerShell bang quyen Administrator roi chay lai:

```powershell
.\start_mongodb.ps1
```

3. Neu van loi, dung mot MongoDB da cai san tren may thay vi binary trong repo.

4. Neu van muon dung binary trong repo, thu copy ca thu muc `Week 7` sang mot duong dan ngan, chi dung ky tu ASCII, vi du:

```text
E:\Code\Week7
```

Sau do chay lai tu thu muc moi.

5. Kiem tra phan mem diet virus / Windows security co dang khoa file trong `mongodb\data` hay khong.

## 7. Cach chay tung file

### `mini_user_api.py`

### Muc dich

API Flask nho, du lieu nam san trong list Python, khong can MongoDB.

### Cach chay

```powershell
python mini_user_api.py
```

Mac dinh Flask chay tai:

```text
http://127.0.0.1:5000
```

### Endpoint co san

- `GET /health`
- `GET /users`
- `GET /users/sample-document`

### Cach test bang PowerShell

```powershell
Invoke-RestMethod http://127.0.0.1:5000/health
Invoke-RestMethod http://127.0.0.1:5000/users
Invoke-RestMethod http://127.0.0.1:5000/users/sample-document
```

### Ket qua mong doi

- `/health` tra ve `{"status":"ok"}`
- `/users` tra ve danh sach 2 user mau
- `/users/sample-document` tra ve 1 user document mau

### Dung server

Nhan `Ctrl + C` trong cua so dang chay Flask.

### `mongo_demo.py`

### Muc dich

Ket noi MongoDB bang `pymongo`, xoa du lieu cu, insert 1 user mau, sau do doc lai.

### Dieu kien

- MongoDB phai dang chay tren `localhost:27017`
- file `.env` hop le

### Cach chay

```powershell
python mongo_demo.py
```

### Ket qua mong doi

Khi thanh cong se in ra:

- thong bao da ket noi MongoDB
- document vua insert

Neu MongoDB chua len, ban se gap `ServerSelectionTimeoutError`.

### `mongo_schema_model_demo.py`

### Muc dich

Demo `Schema` va `Model` bang `mongoengine`.

### Dieu kien

- MongoDB dang chay
- file `.env` hop le

### Cach chay

```powershell
python mongo_schema_model_demo.py
```

### Ket qua mong doi

Script se:

- drop collection `users`
- tao 1 `User`
- in schema va document da luu

### `api_db_mapping_demo.py`

### Muc dich

Mo phong qua trinh:

- API nhan JSON request
- map `_id` thanh `user_id`
- luu xuong MongoDB
- tra response cho client

### Dieu kien

- MongoDB dang chay
- file `.env` hop le

### Cach chay

```powershell
python api_db_mapping_demo.py
```

### Ket qua mong doi

Script se in:

- `API request`
- mapping giua field API va field database
- document luu trong database
- `API response`

### `validation_error_demo.py`

### Muc dich

Demo validation o 2 tang:

- tang API
- tang schema/model

### Dieu kien

- MongoDB dang chay
- file `.env` hop le

### Cach chay

```powershell
python validation_error_demo.py
```

### Ket qua mong doi

Script lan luot in ket qua cho 5 tinh huong:

1. Tao user hop le
2. Thieu field bat buoc
3. Sai format du lieu
4. Trung du lieu unique
5. Khong tim thay du lieu

Cuoi cung se in nhac lai cac ma loi thuong dung: `400`, `404`, `500`.

### `product_crud_api.py`

### Muc dich

API CRUD cho `products` trong MongoDB.

### Dieu kien

- MongoDB dang chay
- file `.env` hop le

### Cach chay

```powershell
python product_crud_api.py
```

Mac dinh Flask chay tai:

```text
http://127.0.0.1:5000
```

### Luu y ve cong

File nay cung dung cong `5000`, giong `mini_user_api.py`.

Vi vay:

- chi nen chay 1 API Flask tai 1 thoi diem
- neu `5000` da bi chiem, dung server cu truoc

Kiem tra port:

```powershell
netstat -ano | findstr :5000
```

### Endpoint

- `GET /health`
- `GET /products`
- `GET /products/<product_id>`
- `POST /products`
- `PUT /products/<product_id>`
- `DELETE /products/<product_id>`

### Test nhanh bang PowerShell

Kiem tra health:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/health
```

Tao product:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:5000/products `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"_id":"p01","name":"Laptop","price":1500}'
```

Lay danh sach product:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/products
```

Lay 1 product:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/products/p01
```

Cap nhat product:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:5000/products/p01 `
  -Method PUT `
  -ContentType "application/json" `
  -Body '{"name":"Laptop Pro","price":1800}'
```

Xoa product:

```powershell
Invoke-WebRequest `
  -Uri http://127.0.0.1:5000/products/p01 `
  -Method DELETE
```

### Loi co the gap

- `500`: MongoDB khong chay hoac khong ket noi duoc
- `404`: khong tim thay product
- `400`: thieu `_id`, `name`, hoac `price` khi tao moi

## 8. File YAML OpenAPI

### `user-api-openapi.yaml`

Day la file mo ta API, khong phai file Python de chay.

Ban co the:

- mo bang VS Code
- paste vao Swagger Editor
- dung de tham khao khi thuyet trinh

### `user-api-openapi-full.yaml`

Tuong tu, day la ban mo rong day du hon cua OpenAPI.

No mo ta:

- server local
- tag `Users`
- schema `User`
- endpoint `/users`
- endpoint `/users/sample-document`

## 9. Thu tu chay de demo tren lop

Neu muon demo tu de den kho, nen chay theo thu tu sau:

1. `mini_user_api.py`
2. `mongo_demo.py`
3. `mongo_schema_model_demo.py`
4. `api_db_mapping_demo.py`
5. `validation_error_demo.py`
6. `product_crud_api.py`

## 10. Lenh tong hop nhanh

```powershell
cd "E:\Code\Kiến trúc hướng dịch vụ\Week 7"
pip install flask pymongo python-dotenv mongoengine
Copy-Item .env.example .env
.\start_mongodb.ps1
python mini_user_api.py
```

Khi muon chay file khac, dung server hien tai roi thay lenh `python ...` bang file can demo.
