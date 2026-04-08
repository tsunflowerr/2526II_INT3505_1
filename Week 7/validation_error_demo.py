import os
import re

from dotenv import load_dotenv
from mongoengine import (
    Document,
    EmailField,
    IntField,
    StringField,
    ValidationError,
    NotUniqueError,
    connect,
    disconnect,
)
from pymongo.errors import ConnectionFailure


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "week7_demo")


class User(Document):
    meta = {"collection": "users"}

    user_id = StringField(required=True, primary_key=True)
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    age = IntField(min_value=0, required=True)


def validate_api_request(request_body):
    required_fields = ["_id", "name", "email", "age"]
    for field in required_fields:
        if field not in request_body:
            return {"status_code": 400, "message": f"Thieu field bat buoc: {field}"}

    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", request_body["email"]):
        return {"status_code": 400, "message": "Email sai format"}

    if not isinstance(request_body["age"], int):
        return {"status_code": 400, "message": "Age phai la so"}

    return None


def create_user_api(request_body):
    api_error = validate_api_request(request_body)
    if api_error:
        return api_error

    try:
        user = User(
            user_id=request_body["_id"],
            name=request_body["name"],
            email=request_body["email"],
            age=request_body["age"],
        )
        user.save()
        return {
            "status_code": 201,
            "data": {
                "_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "age": user.age,
            },
        }
    except ValidationError as error:
        return {"status_code": 400, "message": f"Schema validation error: {error}"}
    except NotUniqueError:
        return {"status_code": 400, "message": "Email da ton tai"}
    except ConnectionFailure:
        return {"status_code": 500, "message": "Loi ket noi database"}
    except Exception as error:
        return {"status_code": 500, "message": f"Loi he thong: {error}"}


def get_user_api(user_id):
    user = User.objects(user_id=user_id).first()
    if not user:
        return {"status_code": 404, "message": "Khong tim thay user"}

    return {
        "status_code": 200,
        "data": {
            "_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "age": user.age,
        },
    }


def main():
    connect(db=MONGO_DB, host=MONGO_URI)
    User.drop_collection()

    valid_request = {
        "_id": "6612abc123",
        "name": "Nguyen Van A",
        "email": "a@gmail.com",
        "age": 22,
    }
    missing_field_request = {
        "_id": "6612abc124",
        "name": "Tran Thi B",
        "age": 21,
    }
    invalid_format_request = {
        "_id": "6612abc125",
        "name": "Le Van C",
        "email": "invalid-email",
        "age": 20,
    }
    duplicate_email_request = {
        "_id": "6612abc126",
        "name": "Pham Thi D",
        "email": "a@gmail.com",
        "age": 23,
    }

    print("1. Tao user hop le")
    print(create_user_api(valid_request))
    print()

    print("2. Thieu field bat buoc")
    print(create_user_api(missing_field_request))
    print()

    print("3. Sai format du lieu")
    print(create_user_api(invalid_format_request))
    print()

    print("4. Trung du lieu unique")
    print(create_user_api(duplicate_email_request))
    print()

    print("5. Khong tim thay du lieu")
    print(get_user_api("not-found"))
    print()

    print("Ma loi thuong dung: 400, 404, 500")

    disconnect()


if __name__ == "__main__":
    main()
