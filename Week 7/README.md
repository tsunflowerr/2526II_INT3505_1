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

Files:
- `mongo_demo.py`: ket noi MongoDB, insert document, doc lai document
- `mongo_schema_model_demo.py`: demo Schema va Model voi `mongoengine`
- `api_db_mapping_demo.py`: demo mapping giua API va database
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

Chay demo Schema va Model:

```bash
python mongo_schema_model_demo.py
```

Chay demo Mapping API va Database:

```bash
python api_db_mapping_demo.py
```
