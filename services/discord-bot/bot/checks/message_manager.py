from discord import app_commands

from bot.config import MESSAGE_MANAGER_ROLE_IDS


def require_message_manager():

    async def predicate(interaction):

        # Allow administrators
        if interaction.user.guild_permissions.administrator:
            return True

        # Allow configured roles
        member = interaction.user

        for role in member.roles:
            if role.id in MESSAGE_MANAGER_ROLE_IDS:
                return True

        raise app_commands.CheckFailure(
            "You don't have permission to use this command."
        )

    return app_commands.check(predicate)