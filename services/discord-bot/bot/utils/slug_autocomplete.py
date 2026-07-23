import discord

from bot.repositories import MessageTemplateRepository

async def message_slug_autocomplete(
    interaction: discord.Interaction,
    current: str
):

    repo = MessageTemplateRepository(
        interaction.client.mongo
    )

    templates = repo.find()

    choices = []

    for item in templates:
        slug = item["slug"]

        if current.lower() in slug.lower():
            choices.append(
                discord.app_commands.Choice(
                    name=slug,
                    value=slug
                )
            )

    return choices[:25]