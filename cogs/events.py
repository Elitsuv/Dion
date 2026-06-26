import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from datetime import datetime
from utils.embeds import DionEmbed
from utils.db import get_connection

class RSVPView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def update_rsvp(self, interaction: discord.Interaction, status: str):
        message_id = interaction.message.id
        user_id = interaction.user.id
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get event ID
        cursor.execute("SELECT event_id FROM events WHERE message_id = ?", (message_id,))
        event = cursor.fetchone()
        if not event:
            conn.close()
            return await interaction.response.send_message("❌ This event is no longer active in the database.", ephemeral=True)
            
        event_id = event[0]
        
        # Insert or update RSVP
        cursor.execute(
            "INSERT OR REPLACE INTO event_rsvps (event_id, user_id, status) VALUES (?, ?, ?)",
            (event_id, user_id, status)
        )
        conn.commit()
        
        # Fetch updated counts
        cursor.execute("SELECT status, COUNT(*) FROM event_rsvps WHERE event_id = ? GROUP BY status", (event_id,))
        counts = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        
        # Re-build the embed
        embed = interaction.message.embeds[0]
        
        # Find the fields and update them
        attending_str = f"✅ Attending: {counts.get('attending', 0)}"
        maybe_str = f"❔ Maybe: {counts.get('maybe', 0)}"
        not_coming_str = f"❌ Not Coming: {counts.get('not_coming', 0)}"
        
        # We assume the RSVP counts are the first field.
        if len(embed.fields) > 0:
            embed.set_field_at(0, name="RSVPs", value=f"{attending_str} | {maybe_str} | {not_coming_str}", inline=False)
        else:
            embed.add_field(name="RSVPs", value=f"{attending_str} | {maybe_str} | {not_coming_str}", inline=False)

        await interaction.response.edit_message(embed=embed)
        # We also send an ephemeral confirmation
        await interaction.followup.send(f"Your RSVP has been recorded as: **{status}**.", ephemeral=True)

    @discord.ui.button(label="Attending", style=discord.ButtonStyle.success, emoji="✅", custom_id="rsvp_attending")
    async def rsvp_attending(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.update_rsvp(interaction, "attending")

    @discord.ui.button(label="Maybe", style=discord.ButtonStyle.secondary, emoji="❔", custom_id="rsvp_maybe")
    async def rsvp_maybe(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.update_rsvp(interaction, "maybe")

    @discord.ui.button(label="Not Coming", style=discord.ButtonStyle.danger, emoji="❌", custom_id="rsvp_not_coming")
    async def rsvp_not_coming(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.update_rsvp(interaction, "not_coming")


class Events(commands.Cog):
    """
    Event scheduling and RSVP system.
    """
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='event_create', description="Create a new event with RSVP buttons.")
    @app_commands.describe(title="Event title", description="Event details", time="Event time (e.g., 'Tonight 8PM')")
    async def event_create(self, interaction: discord.Interaction, title: str, description: str, time: str):
        embed = DionEmbed(
            title=f"📅 {title}",
            description=f"**Details:** {description}\n**Time:** {time}"
        )
        embed.set_author(name=f"Hosted by {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="RSVPs", value="✅ Attending: 0 | ❔ Maybe: 0 | ❌ Not Coming: 0", inline=False)
        
        await interaction.response.send_message("Event created successfully!", ephemeral=True)
        msg = await interaction.channel.send(embed=embed, view=RSVPView())
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO events (guild_id, creator_id, title, description, event_time, message_id) VALUES (?, ?, ?, ?, ?, ?)",
            (interaction.guild.id, interaction.user.id, title, description, time, msg.id)
        )
        conn.commit()
        conn.close()

    @app_commands.command(name='event_list', description="View upcoming events in this server.")
    async def event_list(self, interaction: discord.Interaction):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT event_id, title, event_time FROM events WHERE guild_id = ? ORDER BY event_id DESC LIMIT 10", (interaction.guild.id,))
        events = cursor.fetchall()
        conn.close()
        
        if not events:
            return await interaction.response.send_message("No upcoming events found.", ephemeral=True)
            
        embed = DionEmbed(title="Upcoming Events")
        for e_id, title, e_time in events:
            embed.add_field(name=f"ID: {e_id} | {title}", value=f"Time: {e_time}", inline=False)
            
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='event_cancel', description="Cancel an event by its ID.")
    @app_commands.default_permissions(manage_events=True)
    async def event_cancel(self, interaction: discord.Interaction, event_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT message_id FROM events WHERE event_id = ? AND guild_id = ?", (event_id, interaction.guild.id))
        event = cursor.fetchone()
        
        if not event:
            conn.close()
            return await interaction.response.send_message("❌ Event not found.", ephemeral=True)
            
        cursor.execute("DELETE FROM events WHERE event_id = ?", (event_id,))
        cursor.execute("DELETE FROM event_rsvps WHERE event_id = ?", (event_id,))
        conn.commit()
        conn.close()
        
        # Try to delete the original message
        try:
            msg = await interaction.channel.fetch_message(event[0])
            await msg.delete()
        except discord.NotFound:
            pass # Message already deleted
            
        await interaction.response.send_message(f"✅ Event `{event_id}` has been cancelled.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Events(bot))
    bot.add_view(RSVPView())
