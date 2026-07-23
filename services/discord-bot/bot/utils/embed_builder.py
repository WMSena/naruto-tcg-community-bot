import discord


def build_embed(document: dict) -> discord.Embed:

    embed = discord.Embed(
        title=document.get("title"),
        description=document.get("description"),
        color=document.get("color", 0xF39C12)
    )

    author = document.get("author")
    if author:
        embed.set_author(
            name=author.get("name"),
            url=author.get("url"),
            icon_url=author.get("icon_url")
        )

    thumbnail = document.get("thumbnail")
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    image = document.get("image")
    if image:
        embed.set_image(url=image)

    footer = document.get("footer")
    if footer:
        embed.set_footer(
            text=footer.get("text"),
            icon_url=footer.get("icon_url")
        )

    for field in document.get("fields", []):

        embed.add_field(
            name=field["name"],
            value=field["value"],
            inline=field.get("inline", False)
        )

    return embed