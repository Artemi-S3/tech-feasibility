import os
from typing import List, Optional
from pymongo import MongoClient
from models import ItemIn, ItemOut

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

class MongoBackend:
    def __init__(self) -> None:
        self.client = None
        self.col = None

    def connect(self) -> None:
        self.client = MongoClient(MONGODB_URI)
        db = self.client["artemis3"]
        self.col = db["items"]
        self.col.create_index("name")

    def list_all(self, limit: Optional[int]) -> List[ItemOut]:
        cursor = self.col.find({}).sort([("_id", 1)])
        if limit:
            cursor = cursor.limit(limit)
        return [ItemOut(id=str(d["_id"]), name=d["name"], path=d["path"]) for d in cursor]

    def create_item(self, item: ItemIn) -> ItemOut:
        result = self.col.insert_one({"name": item.name, "path": item.path})
        doc = self.col.find_one({"_id": result.inserted_id})
        return ItemOut(id=str(doc["_id"]), name=doc["name"], path=doc["path"])

    def close(self) -> None:
        if self.client:
            self.client.close()
