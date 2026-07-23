from datetime import datetime, timezone


class MessageTemplateRepository:

    def __init__(self, mongo):
        self.collection = mongo.db.message_template
        
    def find(self):
        return self.collection.find({})

    def get(self, slug: str):
        return self.collection.find_one({
            "slug": slug
        })

    def save(self, document: dict):
        now = datetime.now(timezone.utc)

        slug = document["slug"]

        document["updated_at"] = now

        self.collection.update_one(
            {
                "slug": slug
            },
            {
                "$set": document,
                "$setOnInsert": {
                    "created_at": now
                }
            },
            upsert=True
        )

        return self.get(slug)

    def delete(self, slug: str):
        self.collection.delete_one({
            "slug": slug
        })