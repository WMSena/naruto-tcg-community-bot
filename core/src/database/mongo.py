from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure


class MongoDB:
    """
    Singleton MongoDB connection wrapper.

    Usage:
        mongo = MongoDB(
            uri="mongodb://localhost:27017",
            database="narutotcg"
        )

        mongo.connect()

        mongo.db.message_store.find_one(...)
    """

    def __init__(self, uri: str, database: str):
        self.uri = uri
        self.database_name = database

        self.client: MongoClient | None = None
        self.db: Database | None = None

    def connect(self):
        """
        Connect to MongoDB only once.
        """

        if self.client is not None:
            return

        self.client = MongoClient(self.uri)

        try:
            self.client.admin.command("ping")
        except ConnectionFailure as e:
            raise RuntimeError(
                f"Failed to connect to MongoDB: {e}"
            )

        self.db = self.client[self.database_name]

        print("=" * 50)
        print("MongoDB Connected")
        print(f"Database : {self.database_name}")
        print("=" * 50)

    def close(self):
        """
        Close Mongo connection.
        """

        if self.client is not None:
            self.client.close()

            self.client = None
            self.db = None

            print("MongoDB Connection Closed")