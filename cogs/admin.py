import discord
from discord.ext import commands
from discord import app_commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='clear', description="Deletes a specified number of messages from the channel.")
    @app_commands.default_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int = 5):
        """Deletes a specified number of messages from the channel."""
        # Acknowledge the command first since bulk delete can take time
        await interaction.response.defer(ephemeral=True)
        purged = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f'🧹 Cleaned `{len(purged)}` messages from this sector.', ephemeral=True)

    @app_commands.command(name='alert', description="Broadcasts an engineered global alert to the channel.")
    @app_commands.default_permissions(administrator=True)
    async def alert(self, interaction: discord.Interaction, message: str):
        """Broadcasts an engineered global alert to the channel."""
        embed = discord.Embed(
            title="🚨 SYSTEM ANNOUNCEMENT",
            description=message,
            color=0xFFB347
        )
        embed.set_footer(text=f"Authorized by: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='lock', description="Locks the current text channel, stopping members from typing.")
    @app_commands.default_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        """Locks the current text channel, stopping members from typing."""
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
        embed = discord.Embed(
            description="🔒 **Channel Lockdown Initiated.** Text operations suspended.",
            color=0xFFB347
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='unlock', description="Unlocks the text channel, restoring standard operational permissions.")
    @app_commands.default_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        """Unlocks the text channel, restoring standard operational permissions."""
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
        embed = discord.Embed(
            description="🔓 **Channel Unlocked.** Operations fully restored.",
            color=0xFFB347
        )
        await interaction.response.send_message(embed=embed)

    # Error handling for unauthorized access attempts
    def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            return interaction.response.send_message("🛑 **Access Denied.** Your security clearance is insufficient for this command.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))
