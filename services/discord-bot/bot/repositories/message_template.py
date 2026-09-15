from datetime import datetime, timezone


class MessageTemplateRepository:
    """
    Collection: ``message_template`` (database ``narutotcg``)

    One document per Discord embed template. ``slug`` is the public identifier
    used by ``/messages preview|publish|delete``.

    Document shape (fields consumed by ``build_embed``)::

        {
            "_id": ObjectId,
            "slug": "rules",
            "title": "📜 ...",
            "description": "...",
            "color": 15965202,
            "author": {"name": str, "url": str, "icon_url": str},
            "thumbnail": "https://...",
            "image": "https://...",
            "footer": {"text": str, "icon_url": str},
            "fields": [
                {"name": str, "value": str, "inline": false}
            ],
            "created_at": ISODate("..."),
            "updated_at": ISODate("...")
        }

    Optional embed keys (author, thumbnail, image, footer, fields, color)
    may be omitted. ``color`` is an int; JSON has no hex literals so 0xF39C12
    is stored as 15965202.
    """

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