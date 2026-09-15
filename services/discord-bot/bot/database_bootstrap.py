import copy
from datetime import timezone

from bot.config import (
    DISCORD_GUILD_ID,
    RULES_MESSAGE_CHANNEL_ID,
    RULES_MESSAGE_ID,
)
from bot.data import DEFAULT_MESSAGE_TEMPLATES
from bot.data.default_templates import RULES_PUBLISHED_AT
from bot.repositories import MessageStoreRepository, MessageTemplateRepository


def ensure_indexes(mongo):
    """
    Recreate the lookup indexes the repositories depend on.

    MongoDB does not create collections until the first insert; creating an
    index is enough to materialize an empty collection with the right shape.
    """

    mongo.db.message_template.create_index("slug", unique=True)
    mongo.db.message_store.create_index("key", unique=True)

    print("MongoDB indexes ensured (message_template.slug, message_store.key)")


def seed_default_templates(mongo):
    """Insert reconstructed templates only when the slug is missing."""

    repo = MessageTemplateRepository(mongo)

    for template in DEFAULT_MESSAGE_TEMPLATES:
        slug = template["slug"]
        if repo.get(slug) is not None:
            continue

        repo.save(copy.deepcopy(template))
        print(f"Seeded message_template slug={slug}")


def restore_rules_message_store(
    mongo,
    channel_id: str | None = None,
    message_id: str | None = None,
    guild_id: int | None = None,
    force: bool = False,
):
    """
    Re-attach the live Discord peraturan message so `/messages publish rules`
    edits it instead of posting a duplicate.

    Requires a rules channel id. Guild id comes from DISCORD_GUILD_ID. Message
    id defaults to the recovered snowflake 1529821999977857036.
    """

    channel_id = (channel_id or RULES_MESSAGE_CHANNEL_ID or "").strip()
    message_id = (message_id or RULES_MESSAGE_ID or "").strip()
    guild_id = DISCORD_GUILD_ID if guild_id is None else guild_id

    if not channel_id or not message_id:
        return

    repo = MessageStoreRepository(mongo)
    existing = repo.get("rules")
    if existing is not None and not force:
        return

    repo.save(
        key="rules",
        guild_id=guild_id,
        channel_id=int(channel_id),
        message_id=int(message_id),
    )

    mongo.db.message_store.update_one(
        {"key": "rules"},
        {
            "$set": {
                "created_at": RULES_PUBLISHED_AT.astimezone(timezone.utc),
            }
        },
    )

    print(
        "Restored message_store key=rules "
        f"message_id={message_id} channel_id={channel_id}"
    )


def bootstrap_database(mongo):
    ensure_indexes(mongo)
    seed_default_templates(mongo)
    restore_rules_message_store(mongo)
