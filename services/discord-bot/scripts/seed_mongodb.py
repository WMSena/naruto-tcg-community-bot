#!/usr/bin/env python
"""
Recreate MongoDB collections, indexes, and the reconstructed `rules` documents.

Usage (inside the discord-bot container or venv):

    python scripts/seed_mongodb.py --channel-id YOUR_RULES_CHANNEL_ID

    python scripts/seed_mongodb.py --dump-json

Without --channel-id, only indexes + message_template.rules are created.
`/messages publish rules` would then post a NEW Discord message. Pass the
channel id (Developer Mode → Copy Channel ID) so message_store points at
the existing embed 1529821999977857036 instead.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _json_default(value):
    if isinstance(value, datetime):
        return value.isoformat()
    raise TypeError(f"Not JSON serializable: {type(value)}")


def dump_json():
    from bot.data.default_templates import (
        RULES_MESSAGE_ID,
        RULES_PUBLISHED_AT,
        RULES_TEMPLATE,
    )

    template = {
        **RULES_TEMPLATE,
        "created_at": RULES_PUBLISHED_AT,
        "updated_at": RULES_PUBLISHED_AT,
    }
    store = {
        "key": "rules",
        "guild_id": "<DISCORD_GUILD_ID>",
        "channel_id": "<RULES_MESSAGE_CHANNEL_ID>",
        "message_id": RULES_MESSAGE_ID,
        "created_at": RULES_PUBLISHED_AT,
        "updated_at": RULES_PUBLISHED_AT,
    }
    payload = {
        "database": "narutotcg",
        "collections": {
            "message_template": [template],
            "message_store": [store],
        },
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False, default=_json_default))


def seed(channel_id: str | None, message_id: str | None, force: bool):
    from bot.config import MONGO_DATABASE, MONGO_URI
    from bot.data.default_templates import RULES_MESSAGE_ID
    from bot.database_bootstrap import (
        bootstrap_database,
        restore_rules_message_store,
    )
    from database import MongoDB

    mongo = MongoDB(uri=MONGO_URI, database=MONGO_DATABASE)
    mongo.connect()
    try:
        bootstrap_database(mongo)
        if channel_id:
            restore_rules_message_store(
                mongo,
                channel_id=channel_id,
                message_id=message_id or RULES_MESSAGE_ID,
                force=force,
            )

        print()
        print("message_template.rules:")
        print(mongo.db.message_template.find_one({"slug": "rules"}))
        print()
        print("message_store.rules:")
        print(mongo.db.message_store.find_one({"key": "rules"}))
    finally:
        mongo.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--channel-id",
        help="Discord channel id of the live peraturan message",
    )
    parser.add_argument(
        "--message-id",
        help="Discord message id (default: recovered 1529821999977857036)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing message_store.rules document",
    )
    parser.add_argument(
        "--dump-json",
        action="store_true",
        help="Print reconstructed documents and exit (no Mongo connection)",
    )
    args = parser.parse_args()

    if args.dump_json:
        dump_json()
        return

    seed(args.channel_id, args.message_id, args.force)


if __name__ == "__main__":
    main()
