import os

from dotenv import load_dotenv
from mongoengine import Document, IntField, StringField, connect, disconnect


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "week7_demo")


class User(Document):
    meta = {"collection": "users"}

    user_id = StringField(required=True, primary_key=True)
    name = StringField(required=True, max_length=100)
    email = StringField(required=True)
    age = IntField(min_value=0)


def main():
    connect(db=MONGO_DB, host=MONGO_URI)

    User.drop_collection()

    user = User(
        user_id="6612abc123",
        name="Nguyen Van A",
        email="a@gmail.com",
        age=22,
    )
    user.save()

    saved_user = User.objects(user_id="6612abc123").first()

    print("Schema: user_id, name, email, age")
    print("Model: User")
    print(saved_user.to_mongo().to_dict())

    disconnect()


if __name__ == "__main__":
    main()
