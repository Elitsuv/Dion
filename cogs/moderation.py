import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import sqlite3
from utils.embeds import DionEmbed
from utils.db import get_connection

class Moderation(commands.Cog):
    """
    Moderation commands for Dion Corp.
    """
    def __init__(self, bot):
        self.bot = bot

    def log_action(self, user_id, moderator_id, reason, action_type="warn"):
        conn = get_connection()
        cursor = conn.cursor()
        formatted_reason = f"[{action_type.upper()}] {reason}"
        cursor.execute(
            "INSERT INTO warnings (user_id, moderator_id, reason) VALUES (?, ?, ?)",
            (user_id, moderator_id, formatted_reason)
        )
        conn.commit()
        conn.close()

    @app_commands.command(name='warn', description="Warn a user.")
    @app_commands.default_permissions(moderate_members=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        self.log_action(member.id, interaction.user.id, reason, "warn")
        embed = DionEmbed(
            title="⚠️ Warning Issued",
            description=f"**Target:** {member.mention}\n**Reason:** {reason}"
        )
        embed.set_footer(text=f"Authorized by: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        
        try:
            await member.send(f"You have been warned in **{interaction.guild.name}** for: {reason}")
        except discord.Forbidden:
            pass
            
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='warnings', description="View warnings for a user.")
    @app_commands.default_permissions(moderate_members=True)
    async def warnings(self, interaction: discord.Interaction, member: discord.Member):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT warn_id, moderator_id, reason, timestamp FROM warnings WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10", (member.id,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return await interaction.response.send_message(f"✅ {member.mention} has no warnings.", ephemeral=True)

        embed = DionEmbed(title=f"Modlogs: {member.name}")
        for warn_id, mod_id, reason, timestamp in rows:
            mod = self.bot.get_user(mod_id)
            mod_name = mod.name if mod else f"Unknown ({mod_id})"
            embed.add_field(name=f"ID: {warn_id} | By: {mod_name}", value=f"{reason}\n*{timestamp}*", inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='modlogs', description="Alias for /warnings.")
    @app_commands.default_permissions(moderate_members=True)
    async def modlogs(self, interaction: discord.Interaction, member: discord.Member):
        await self.warnings.callback(self, interaction, member)

    @app_commands.command(name='timeout', description="Time out a user.")
    @app_commands.default_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "No reason provided."):
        try:
            duration = timedelta(minutes=minutes)
            await member.timeout(duration, reason=reason)
            self.log_action(member.id, interaction.user.id, reason, "timeout")
            
            embed = DionEmbed(
                title="⏱️ Timeout Issued",
                description=f"**Target:** {member.mention}\n**Duration:** `{minutes} minutes`\n**Reason:** {reason}"
            )
            embed.set_footer(text=f"Authorized by: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Error: I do not have permission to time out this user.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {e}", ephemeral=True)

    @app_commands.command(name='kick', description="Kicks a user.")
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
        try:
            await member.kick(reason=reason)
            self.log_action(member.id, interaction.user.id, reason, "kick")
            
            embed = DionEmbed(
                title="👢 Kick Issued",
                description=f"**Target:** {member.mention}\n**Reason:** {reason}"
            )
            embed.set_footer(text=f"Authorized by: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Error: I do not have permission to kick this user.", ephemeral=True)

    @app_commands.command(name='ban', description="Bans a user.")
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
        try:
            await member.ban(reason=reason)
            self.log_action(member.id, interaction.user.id, reason, "ban")
            
            embed = DionEmbed(
                title="🔨 Ban Issued",
                description=f"**Target:** {member.mention}\n**Reason:** {reason}"
            )
            embed.set_footer(text=f"Authorized by: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Error: I do not have permission to ban this user.", ephemeral=True)

    @app_commands.command(name='purge', description="Deletes a specified number of messages.")
    @app_commands.default_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int = 5):
        await interaction.response.defer(ephemeral=True)
        purged = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f'🧹 Purged `{len(purged)}` messages.', ephemeral=True)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
