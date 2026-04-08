# Week 7 - Demo MongoDB Document, Schema, Model

```json
{
  "_id": "6612abc123",
  "name": "Nguyen Van A",
  "email": "a@gmail.com",
  "age": 22
}
```

Demo nho ket noi MongoDB:
- Mỗi `user` la mot document trong collection `users`
- `_id` la khoa dinh danh duy nhat
- Cac truong con lai luu thong tin nguoi dung

Demo Schema va Model:
- `Schema`: cac field cua `User` gom `user_id`, `name`, `email`, `age`
- `Model`: class `User` dung de luu va truy van document

Demo Mapping giua API va Database:
- API nhan JSON request
- Server map du lieu request sang `User model`
- `User model` duoc luu thanh document trong MongoDB
- Sau do server tra JSON response ve client

Validation va xu ly loi:
- Validate o tang API: kiem tra field bat buoc, kieu du lieu, format email
- Validate o tang schema/model: kiem tra rang buoc `required`, `min`, `unique`
- Loi thuong gap: thieu field, sai format, trung du lieu unique, loi ket noi DB
- API nen tra ma loi phu hop: `400`, `404`, `500`

Ly thuyet ngan gon cho slide:
- Validation giup kiem tra du lieu truoc khi luu vao database
- Tang API xu ly cac loi de nhin thay ngay tu request
- Tang schema/model dam bao du lieu vao database dung cau truc
- Xu ly loi dung ma trang thai giup client de hieu va de debug

Files:
- `mongo_demo.py`: ket noi MongoDB, insert document, doc lai document
- `mongo_schema_model_demo.py`: demo Schema va Model voi `mongoengine`
- `api_db_mapping_demo.py`: demo mapping giua API va database
- `validation_error_demo.py`: demo validation va xu ly loi
- `product_crud_api.py`: CRUD Product voi Flask + MongoDB
- `start_mongodb.ps1`: bat MongoDB local
- `stop_mongodb.ps1`: tat MongoDB local
- `.env.example`: file env mau

Cai thu vien:

```bash
pip install pymongo python-dotenv mongoengine
```

Tao file `.env` tu `.env.example`:

```env
MONGO_URI=mongodb://localhost:27017/
MONGO_DB=week7_demo
MONGO_COLLECTION=users
```

Chay demo:

```bash
python mongo_demo.py
```

Bat MongoDB local:

```powershell
.\\start_mongodb.ps1
```

Tat MongoDB local:

```powershell
.\\stop_mongodb.ps1
```

Chay demo Schema va Model:

```bash
python mongo_schema_model_demo.py
```

Chay demo Mapping API va Database:

```bash
python api_db_mapping_demo.py
```

Chay demo Validation va xu ly loi:

```bash
python validation_error_demo.py
```

CRUD Product:
- `GET /products`: lay danh sach product
- `GET /products/<id>`: lay product theo id
- `POST /products`: tao product moi
- `PUT /products/<id>`: cap nhat product
- `DELETE /products/<id>`: xoa product

Chay API Product:

```bash
python product_crud_api.py
```

Luu y:
- Can MongoDB dang chay tai `mongodb://localhost:27017/` hoac cau hinh lai trong `.env`
- Neu MongoDB chua chay, cac endpoint Product se tra loi `500`

JSON mau:

```json
{
  "_id": "p01",
  "name": "Laptop",
  "price": 1500
}
```
