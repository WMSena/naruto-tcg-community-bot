import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))

MONGO_HOST = os.getenv("MONGO_HOST", "kage").strip() or "kage"
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "narutotcg").strip() or "narutotcg"
MONGO_AUTH_SOURCE = os.getenv("MONGO_AUTH_SOURCE", "admin").strip() or "admin"
MONGO_USERNAME = (
    os.getenv("MONGO_USERNAME", "").strip()
    or os.getenv("MONGO_INITDB_ROOT_USERNAME", "").strip()
)
MONGO_PASSWORD = (
    os.getenv("MONGO_PASSWORD", "").strip()
    or os.getenv("MONGO_INITDB_ROOT_PASSWORD", "").strip()
)


def _mongo_uri() -> str:
    """
    Prefer username/password so the bot can reach `kage` with auth.

    `MONGO_URI=mongodb://kage:27017` (no user) is prioritized
    even when password is set.
    """

    explicit = os.getenv("MONGO_URI", "").strip()
    if explicit:
        return explicit

    if MONGO_USERNAME and MONGO_PASSWORD:
        user = quote_plus(MONGO_USERNAME)
        password = quote_plus(MONGO_PASSWORD)
        auth_source = quote_plus(MONGO_AUTH_SOURCE)
        return (
            f"mongodb://{user}:{password}@{MONGO_HOST}:27017/"
            f"{MONGO_DATABASE}?authSource={auth_source}"
        )

    return f"mongodb://{MONGO_HOST}:27017/{MONGO_DATABASE}"


MONGO_URI = _mongo_uri()
MESSAGE_MANAGER_ROLE_IDS = [
    int(role.strip())
    for role in os.getenv(
        "MESSAGE_MANAGER_ROLE_IDS",
        ""
    ).split(",")
    if role.strip()
]

# Optional recovery of the live peraturan Discord message after DB loss.
# Enable Developer Mode in Discord, right-click the rules channel → Copy Channel ID.
RULES_MESSAGE_CHANNEL_ID = os.getenv("RULES_MESSAGE_CHANNEL_ID", "").strip()
RULES_MESSAGE_ID = os.getenv(
    "RULES_MESSAGE_ID",
    "1529821999977857036",
).strip()
