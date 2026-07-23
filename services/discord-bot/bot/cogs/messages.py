import discord
from discord import app_commands
from discord.ext import commands
from bot.services.message_manager_service import MessageManagerService
from bot.utils.slug_autocomplete import message_slug_autocomplete
from bot.checks import require_message_manager

class Messages(commands.Cog):
    messages = app_commands.Group(
        name="messages",
        description="Manage server messages"
    )
    def __init__(self, bot):
        self.bot = bot
        self.service = MessageManagerService(bot)
        # self.template_repo = MessageTemplateRepository(bot.mongo)
        # self.slug_autocomplete = message_slug_autocomplete(self.template_repo)

    async def cog_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
                ephemeral=True
            )
            return

        raise error
    
    @messages.command(
        name="preview",
        description="Preview a message template"
    )
    @app_commands.describe(
        slug="Message template slug"
    )
    @app_commands.autocomplete(
        slug=message_slug_autocomplete
    )
    async def preview(
        self,
        interaction: discord.Interaction,
        slug: str
    ):
        try:
            embed = await self.service.preview(slug)
            await interaction.response.send_message( embed=embed, ephemeral=True )
        except Exception as e:
            await interaction.response.send_message( str(e), ephemeral=True )

    @messages.command(
        name="publish",
        description="Publish or update a message"
    )
    @app_commands.describe(
        slug="Message template slug"
    )
    @app_commands.autocomplete(
        slug=message_slug_autocomplete
    )
    @require_message_manager()
    async def publish(
        self,
        interaction: discord.Interaction,
        slug: str
    ):
        try:
            result = await self.service.publish(slug, interaction )
            await interaction.response.send_message( result, ephemeral=True )
        except Exception as e:
            await interaction.response.send_message( str(e), ephemeral=True )

    @messages.command(
        name="delete",
        description="Delete managed message"
    )
    @app_commands.describe(
        slug="Message template slug"
    )
    @app_commands.autocomplete(
        slug=message_slug_autocomplete
    )
    @require_message_manager()
    async def delete(
        self,
        interaction: discord.Interaction,
        slug: str
    ):
        try:
            result = await self.service.delete(
                slug
            )
            await interaction.response.send_message(
                result,
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                str(e),
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Messages(bot))