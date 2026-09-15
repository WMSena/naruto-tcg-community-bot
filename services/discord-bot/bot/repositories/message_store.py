from datetime import datetime, timezone


class MessageStoreRepository:
    """
    Collection: ``message_store`` (database ``narutotcg``)

    One document per published managed message. ``key`` is the template slug.

    Document shape::

        {
            "_id": ObjectId,
            "key": "rules",
            "guild_id": "123456789012345678",
            "channel_id": "123456789012345678",
            "message_id": "1529821999977857036",
            "created_at": ISODate("2026-07-23T12:06:27.513Z"),
            "updated_at": ISODate("...")
        }

    Discord snowflakes are stored as strings. Lookups use ``key``.
    """

    def __init__(self, mongo):
        self.collection = mongo.db.message_store

    def get(self, key: str):
        return self.collection.find_one({
            "key": key
        })

    def save(
        self,
        key: str,
        guild_id: int,
        channel_id: int,
        message_id: int
    ):
        now = datetime.now(timezone.utc)

        self.collection.update_one(
            {
                "key": key
            },
            {
                "$set": {
                    "guild_id": str(guild_id),
                    "channel_id": str(channel_id),
                    "message_id": str(message_id),
                    "updated_at": now
                },
                "$setOnInsert": {
                    "created_at": now
                }
            },
            upsert=True
        )

        return self.get(key)

    def delete(self, key: str):
        self.collection.delete_one({
            "key": key
        })