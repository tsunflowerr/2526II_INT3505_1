import os

from dotenv import load_dotenv
from mongoengine import Document, IntField, StringField, connect, disconnect


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "week7_demo")


class User(Document):
    meta = {"collection": "users"}

    user_id = StringField(required=True, primary_key=True)
    name = StringField(required=True)
    email = StringField(required=True)
    age = IntField(min_value=0)


def create_user_api(request_body):
    user = User(
        user_id=request_body["_id"],
        name=request_body["name"],
        email=request_body["email"],
        age=request_body["age"],
    )
    user.save()

    response_body = {
        "_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "age": user.age,
    }
    return response_body


def main():
    connect(db=MONGO_DB, host=MONGO_URI)

    User.drop_collection()

    api_request = {
        "_id": "6612abc123",
        "name": "Nguyen Van A",
        "email": "a@gmail.com",
        "age": 22,
    }

    api_response = create_user_api(api_request)

    saved_user = User.objects(user_id="6612abc123").first()

    print("API request:")
    print(api_request)
    print()
    print("Mapping API -> Database:")
    print("_id -> user_id")
    print("name -> name")
    print("email -> email")
    print("age -> age")
    print()
    print("Document trong database:")
    print(saved_user.to_mongo().to_dict())
    print()
    print("API response:")
    print(api_response)

    disconnect()


if __name__ == "__main__":
    main()
