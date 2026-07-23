import discord

from discord.ext import commands
from discord import app_commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="Check whether the bot is alive."
    )
    async def ping(
        self,
        interaction: discord.Interaction
    ):
        from bot.repositories import MessageStoreRepository

        repo = MessageStoreRepository(self.bot.mongo)

        document = repo.get("rules")

        print(document)

        await interaction.response.send_message(
            "🏓 Pong!"
        )

async def setup(bot):
    await bot.add_cog(Ping(bot))