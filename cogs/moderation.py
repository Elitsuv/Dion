import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
from utils.embeds import DionEmbed
from utils.db import get_db

class Moderation(commands.Cog):
    """
    Moderation commands for Dion Corp.
    """
    def __init__(self, bot):
        self.bot = bot

    def log_action(self, user_id, moderator_id, reason, action_type="warn"):
        from datetime import datetime, timezone, timedelta
        ist = timezone(timedelta(hours=5, minutes=30))
        db = get_db()
        formatted_reason = f"[{action_type.upper()}] {reason}"
        timestamp = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")
        db.add_warning(user_id, moderator_id, formatted_reason, timestamp)

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
        db = get_db()
        user_warnings = db.get_warnings(member.id)
        
        # Sort by timestamp desc and limit 10
        user_warnings.sort(key=lambda x: x["timestamp"], reverse=True)
        user_warnings = user_warnings[:10]

        if not user_warnings:
            return await interaction.response.send_message(f"✅ {member.mention} has no warnings.", ephemeral=True)

        embed = DionEmbed(title=f"Modlogs: {member.name}")
        for w in user_warnings:
            mod = self.bot.get_user(int(w["moderator_id"]))
            mod_name = mod.name if mod else f"Unknown ({w['moderator_id']})"
            embed.add_field(name=f"ID: {w['warn_id']} | By: {mod_name}", value=f"{w['reason']}\n*{w['timestamp']}*", inline=False)

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
