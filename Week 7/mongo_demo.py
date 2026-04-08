import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "week7_demo")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "users")


def main():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    users = db[MONGO_COLLECTION]

    sample_user = {
        "_id": "6612abc123",
        "name": "Nguyen Van A",
        "email": "a@gmail.com",
        "age": 22,
    }

    users.delete_many({})
    users.insert_one(sample_user)

    user = users.find_one({"_id": "6612abc123"})
    print("Da ket noi MongoDB thanh cong")
    print(user)

    client.close()


if __name__ == "__main__":
    main()
