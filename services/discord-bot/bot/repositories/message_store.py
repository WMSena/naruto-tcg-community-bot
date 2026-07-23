from datetime import datetime, timezone


class MessageStoreRepository:

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