import discord
# from discord.errors import NotFound
from datetime import datetime, timezone

from bot.repositories import MessageStoreRepository, MessageTemplateRepository
from bot.utils.embed_builder import build_embed

class MessageManagerService:
    def __init__( self, bot ):
        self.bot = bot
        self.repo = MessageStoreRepository(bot.mongo)
        self.template_repo = MessageTemplateRepository(bot.mongo)

    def _now(self):
        return datetime.now(timezone.utc)

    async def preview(self, slug: str):
        template = self.template_repo.get(slug)
        if template is None:
            raise RuntimeError(f"{slug} template not found.")
        embed = build_embed(template)
        return embed
    
    async def publish(self, slug: str, interaction: discord.Interaction):
        template = self.template_repo.get(slug)
        if template is None:
            raise RuntimeError(f"{slug} template not found.")
        embed = build_embed(template)
        document = self.repo.get(slug)
        
        if interaction.guild is None:
            raise RuntimeError(
                "This command only works inside server."
            )
        # First publish
        if document is None:
            message = await interaction.channel.send(embed=embed)
            self.repo.save(
                key=slug,
                guild_id=interaction.guild.id,
                channel_id=interaction.channel.id,
                message_id=message.id
            )
            return f"{slug} published."

        # Existing message
        channel = self.bot.get_channel(int(document["channel_id"]))
        if channel is None:
            channel = await self.bot.fetch_channel(
                int(document["channel_id"])
            )

        if channel is None:
            raise RuntimeError(f"{slug} channel not found.")
        try:
            message = await channel.fetch_message(
                int(document["message_id"])
            )
            await message.edit(
                embed=embed
            )
            self.repo.save(
                key=slug,
                guild_id=interaction.guild.id,
                channel_id=channel.id,
                message_id=message.id
            )
            return f"{slug} updated."
        except discord.errors.NotFound:
            message = await channel.send(
                embed=embed
            )
            self.repo.save(
                key=slug,
                guild_id=interaction.guild.id,
                channel_id=channel.id,
                message_id=message.id
            )
            return f"{slug} recreated."

    async def delete(self, slug: str):
        document = self.repo.get(slug)
        if document is None:
            return f"{slug} not found."
        channel = self.bot.get_channel(int(document["channel_id"]))
        if channel:
            try:
                message = await channel.fetch_message(int(document["message_id"]))
                await message.delete()
            except discord.errors.NotFound:
                pass
        self.repo.delete(slug)
        return f"{slug} deleted."