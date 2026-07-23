import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017"
)

MONGO_DATABASE = os.getenv(
    "MONGO_DATABASE",
    "narutotcg"
)
MESSAGE_MANAGER_ROLE_IDS = [
    int(role.strip())
    for role in os.getenv(
        "MESSAGE_MANAGER_ROLE_IDS",
        ""
    ).split(",")
    if role.strip()
]