import discord
from discord.ext import commands
from pathlib import Path

from bot.config import (
    DISCORD_GUILD_ID,
    MONGO_URI,
    MONGO_DATABASE
)

from database import MongoDB
from bot.database_bootstrap import bootstrap_database

class NarutoBot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        # intents.members = True
        # intents.message_content = True

        super().__init__(
            command_prefix="!",
            intents=intents
        )

        self.guild_id = DISCORD_GUILD_ID

        # Shared services
        self.mongo = MongoDB(
            uri=MONGO_URI,
            database=MONGO_DATABASE
        )

    async def setup_hook(self):
        # Connect Mongo only once, then recreate indexes + seed missing templates
        self.mongo.connect()
        bootstrap_database(self.mongo)

        # Load all cogs
        await self.load_cogs()

        guild = discord.Object(id=self.guild_id)

        # Copy global commands into the guild
        self.tree.copy_global_to(guild=guild)

        # Sync the guild
        synced = await self.tree.sync(guild=guild)

        print()
        print(f"✅ Synced {len(synced)} guild command(s)")
        print()

    async def close(self):
        self.mongo.close()
        await super().close()

    async def load_cogs(self):
        cogs_path = Path(__file__).parent / "cogs"
        for file in cogs_path.glob("*.py"):
            if file.name.startswith("_"):
                continue

            module = f"bot.cogs.{file.stem}"
            try:
                await self.load_extension(module)
                print(f"✅ Loaded {module}")
            except commands.errors.NoEntryPointError:
                print(f"⏭ Skipped {module} (no setup function)")