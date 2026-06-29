import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import DionEmbed
from utils.db import get_db

class Alerts(commands.Cog):
    """
    Opt-in Alerts and Subscriptions Cog.
    Allows users to subscribe to role-based notifications.
    """
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='alert_create', description="Create a new alert topic and its role (Admin only).")
    @app_commands.describe(name="Name of the alert topic")
    @app_commands.default_permissions(manage_roles=True)
    async def alert_create(self, interaction: discord.Interaction, name: str):
        guild = interaction.guild
        db = get_db()
        
        name_clean = name.strip().lower()
        if not name_clean.isalnum():
            return await interaction.response.send_message("❌ Alert name must contain only alphanumeric characters.", ephemeral=True)
            
        existing = db.get_alert_topic(guild.id, name_clean)
        if existing:
            return await interaction.response.send_message(f"❌ An alert topic named `{name_clean}` already exists.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)

        try:
            # Create a corresponding role
            role_name = f"Alert - {name.strip()}"
            role = await guild.create_role(
                name=role_name,
                mentionable=True,
                reason=f"Dion Opt-in Alerts system created by {interaction.user.name}"
            )
            
            db.add_alert_topic(guild.id, name_clean, role.id)
            
            embed = DionEmbed(
                title="Alert Topic Created",
                description=f"Successfully created alert topic **{name_clean}**.\nAssociated role: {role.mention}"
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to create alert topic: {e}", ephemeral=True)

    @app_commands.command(name='alert_delete', description="Delete an alert topic and its role (Admin only).")
    @app_commands.describe(name="Name of the alert topic")
    @app_commands.default_permissions(manage_roles=True)
    async def alert_delete(self, interaction: discord.Interaction, name: str):
        guild = interaction.guild
        db = get_db()
        name_clean = name.strip().lower()
        
        await interaction.response.defer(ephemeral=True)
        
        role_id = db.remove_alert_topic(guild.id, name_clean)
        if role_id is None:
            return await interaction.followup.send(f"❌ Alert topic `{name_clean}` not found in the database.", ephemeral=True)
            
        # Try to delete the role from the guild
        role = guild.get_role(role_id)
        role_status = ""
        if role:
            try:
                await role.delete(reason=f"Alert topic '{name_clean}' deleted by {interaction.user.name}")
                role_status = "and its corresponding guild role was deleted"
            except discord.Forbidden:
                role_status = f"but I did not have permission to delete the guild role: {role.name}"
            except Exception as e:
                role_status = f"but failed to delete the guild role: {e}"
        else:
            role_status = "and the guild role was already missing or deleted"

        embed = DionEmbed(
            title="Alert Topic Deleted",
            description=f"Successfully deleted alert topic **{name_clean}** {role_status}."
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name='alert_list', description="List all available alert topics.")
    async def alert_list(self, interaction: discord.Interaction):
        db = get_db()
        topics = db.get_alert_topics(interaction.guild.id)
        
        if not topics:
            return await interaction.response.send_message("No alert topics configured for this server.", ephemeral=True)
            
        embed = DionEmbed(title="Available Alert Topics")
        desc = "Join any topic to get notified when announcements are sent!\n\n"
        for t in topics:
            role = interaction.guild.get_role(t["role_id"])
            role_mention = role.mention if role else f"Missing Role (ID: {t['role_id']})"
            desc += f"• **{t['name']}** - {role_mention}\n"
            
        embed.description = desc
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name='alert_join', description="Join/Subscribe to an alert topic.")
    @app_commands.describe(name="Name of the alert topic")
    async def alert_join(self, interaction: discord.Interaction, name: str):
        db = get_db()
        name_clean = name.strip().lower()
        topic = db.get_alert_topic(interaction.guild.id, name_clean)
        
        if not topic:
            return await interaction.response.send_message(f"❌ Alert topic `{name_clean}` does not exist.", ephemeral=True)
            
        role = interaction.guild.get_role(topic["role_id"])
        if not role:
            return await interaction.response.send_message("❌ The role associated with this topic has been deleted or is missing.", ephemeral=True)
            
        if role in interaction.user.roles:
            return await interaction.response.send_message(f"ℹ️ You are already subscribed to `{name_clean}`.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)
        try:
            await interaction.user.add_roles(role, reason="Subscribed to alert topic")
            await interaction.followup.send(f"✅ Successfully subscribed to **{name_clean}**! You will now receive notifications for this topic.", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("❌ I do not have permission to manage roles for you. Make sure my role is above the alert role.", ephemeral=True)

    @app_commands.command(name='alert_leave', description="Leave/Unsubscribe from an alert topic.")
    @app_commands.describe(name="Name of the alert topic")
    async def alert_leave(self, interaction: discord.Interaction, name: str):
        db = get_db()
        name_clean = name.strip().lower()
        topic = db.get_alert_topic(interaction.guild.id, name_clean)
        
        if not topic:
            return await interaction.response.send_message(f"❌ Alert topic `{name_clean}` does not exist.", ephemeral=True)
            
        role = interaction.guild.get_role(topic["role_id"])
        if not role:
            return await interaction.response.send_message("❌ The role associated with this topic has been deleted or is missing.", ephemeral=True)
            
        if role not in interaction.user.roles:
            return await interaction.response.send_message(f"ℹ️ You are not subscribed to `{name_clean}`.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)
        try:
            await interaction.user.remove_roles(role, reason="Unsubscribed from alert topic")
            await interaction.followup.send(f"✅ Successfully unsubscribed from **{name_clean}**.", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("❌ I do not have permission to manage roles for you. Make sure my role is above the alert role.", ephemeral=True)

    @app_commands.command(name='alert_send', description="Send an alert announcement to a topic (Admin only).")
    @app_commands.describe(name="Name of the alert topic", message="The announcement message")
    @app_commands.default_permissions(mention_everyone=True)
    async def alert_send(self, interaction: discord.Interaction, name: str, message: str):
        db = get_db()
        name_clean = name.strip().lower()
        topic = db.get_alert_topic(interaction.guild.id, name_clean)
        
        if not topic:
            return await interaction.response.send_message(f"❌ Alert topic `{name_clean}` does not exist.", ephemeral=True)
            
        role = interaction.guild.get_role(topic["role_id"])
        if not role:
            return await interaction.response.send_message("❌ The role associated with this topic has been deleted or is missing.", ephemeral=True)
            
        await interaction.response.defer(ephemeral=True)
        
        embed = DionEmbed(
            title=f"Announcement: {name_clean.upper()}",
            description=message
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        
        # Send announcement pinging the role
        await interaction.channel.send(content=role.mention, embed=embed)
        await interaction.followup.send(f"✅ Announcement sent to {role.mention}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Alerts(bot))
