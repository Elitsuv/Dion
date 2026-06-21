import discord
from discord.ext import commands
from discord import app_commands
import os

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

    @app_commands.command(name='changelog', description="Post a beautifully formatted bot changelog announcement.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        version="The version number (e.g., v1.1.0)",
        changes="The changes list, use ';' to separate different items.",
        channel="Optional target channel. Uses CHANGELOG_CHANNEL_ID env var or current channel as fallback."
    )
    async def changelog(self, interaction: discord.Interaction, version: str, changes: str, channel: discord.TextChannel = None):
        """Post a beautifully formatted bot changelog announcement."""
        # Determine target channel
        target_channel = channel
        if not target_channel:
            env_channel_id = os.getenv('CHANGELOG_CHANNEL_ID')
            if env_channel_id:
                try:
                    target_channel = self.bot.get_channel(int(env_channel_id))
                except ValueError:
                    pass
        if not target_channel:
            target_channel = interaction.channel

        # Format changes list
        change_items = [item.strip() for item in changes.split(';') if item.strip()]
        formatted_changes = "\n".join([f"• {item}" for item in change_items])

        embed = discord.Embed(
            title=f"🚀 Version Update: {version}",
            color=0xFFB347
        )
        embed.add_field(name="What's New:", value=formatted_changes or "No details provided.", inline=False)
        embed.set_footer(text=f"Updates compiled by: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        
        try:
            await target_channel.send(embed=embed)
            await interaction.response.send_message(f"✅ Changelog posted successfully to {target_channel.mention}!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to send message to {target_channel.mention}: {e}", ephemeral=True)

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
