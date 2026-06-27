import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from datetime import datetime, timedelta
from utils.embeds import DionEmbed
from utils.db import get_db

class RSVPView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def update_rsvp(self, interaction: discord.Interaction, status: str):
        message_id = interaction.message.id
        user_id = interaction.user.id
        
        db = get_db()
        
        event = next((e for e in db.data["events"] if e["message_id"] == message_id), None)
        if not event:
            return await interaction.response.send_message("❌ This event is no longer active in the database.", ephemeral=True)
            
        event_id = event["event_id"]
        
        db.data["event_rsvps"] = [r for r in db.data["event_rsvps"] if not (r["event_id"] == event_id and r["user_id"] == user_id)]
        db.data["event_rsvps"].append({
            "event_id": event_id,
            "user_id": user_id,
            "status": status
        })
        db.save()
        
        counts = {"attending": 0, "maybe": 0, "not_coming": 0}
        for r in db.data["event_rsvps"]:
            if r["event_id"] == event_id:
                counts[r["status"]] = counts.get(r["status"], 0) + 1
        
        embed = interaction.message.embeds[0]
        
        attending_str = f"✅ Attending: {counts.get('attending', 0)}"
        maybe_str = f"❔ Maybe: {counts.get('maybe', 0)}"
        not_coming_str = f"❌ Not Coming: {counts.get('not_coming', 0)}"
        
        if len(embed.fields) > 0:
            embed.set_field_at(0, name="RSVPs", value=f"{attending_str} | {maybe_str} | {not_coming_str}", inline=False)
        else:
            embed.add_field(name="RSVPs", value=f"{attending_str} | {maybe_str} | {not_coming_str}", inline=False)

        await interaction.response.edit_message(embed=embed)
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

    def parse_time(self, time_str: str) -> datetime:
        """Simple time parser for strings like '2h', '30m'."""
        time_str = time_str.lower()
        now = datetime.utcnow()
        if time_str.endswith('h'):
            return now + timedelta(hours=int(time_str[:-1]))
        elif time_str.endswith('m'):
            return now + timedelta(minutes=int(time_str[:-1]))
        elif time_str.endswith('d'):
            return now + timedelta(days=int(time_str[:-1]))
        else:
            raise ValueError("Invalid time format. Use something like 2h, 30m, 1d.")

    async def event_timer(self, channel, message_id, delay, title):
        await asyncio.sleep(delay)
        
        db = get_db()
        event = next((e for e in db.data["events"] if e["message_id"] == message_id), None)
        if not event:
            return
            
        event_id = event["event_id"]
        attendees = [r["user_id"] for r in db.data["event_rsvps"] if r["event_id"] == event_id and r["status"] == "attending"]
        
        db.data["events"] = [e for e in db.data["events"] if e["event_id"] != event_id]
        db.data["event_rsvps"] = [r for r in db.data["event_rsvps"] if r["event_id"] != event_id]
        db.save()
        
        mentions = " ".join([f"<@{uid}>" for uid in attendees])
        if not mentions:
            mentions = "No one RSVP'd 'Attending'."
            
        await channel.send(f"🔔 **Event Starting:** {title}!\n{mentions}")

    @app_commands.command(name='event_create', description="Create a new event with RSVP buttons.")
    @app_commands.describe(title="Event title", description="Event details", duration="Time until event (e.g., '2h', '30m')")
    async def event_create(self, interaction: discord.Interaction, title: str, description: str, duration: str):
        try:
            trigger_time = self.parse_time(duration)
        except ValueError as e:
            return await interaction.response.send_message(f"❌ {e}", ephemeral=True)
            
        timestamp = int(trigger_time.timestamp())
        embed = DionEmbed(
            title=f"📅 {title}",
            description=f"**Details:** {description}\n**Time:** <t:{timestamp}:F> (<t:{timestamp}:R>)"
        )
        embed.set_author(name=f"Hosted by {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="RSVPs", value="✅ Attending: 0 | ❔ Maybe: 0 | ❌ Not Coming: 0", inline=False)
        
        await interaction.response.send_message("Event created successfully!", ephemeral=True)
        msg = await interaction.channel.send(embed=embed, view=RSVPView())
        
        db = get_db()
        event_id = int(datetime.utcnow().timestamp() * 1000)
        
        db.data["events"].append({
            "event_id": event_id,
            "guild_id": interaction.guild.id,
            "creator_id": interaction.user.id,
            "title": title,
            "description": description,
            "event_time": str(timestamp),
            "message_id": msg.id
        })
        db.save()
        
        delay = (trigger_time - datetime.utcnow()).total_seconds()
        if delay > 0:
            self.bot.loop.create_task(self.event_timer(interaction.channel, msg.id, delay, title))

    @app_commands.command(name='event_list', description="View upcoming events in this server.")
    async def event_list(self, interaction: discord.Interaction):
        db = get_db()
        guild_events = [e for e in db.data["events"] if e["guild_id"] == interaction.guild.id][-10:]
        
        if not guild_events:
            return await interaction.response.send_message("No upcoming events found.", ephemeral=True)
            
        embed = DionEmbed(title="Upcoming Events")
        for e in reversed(guild_events):
            embed.add_field(name=f"ID: {e['event_id']} | {e['title']}", value=f"Time: <t:{e['event_time']}:F>", inline=False)
            
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='event_cancel', description="Cancel an event by its ID.")
    @app_commands.default_permissions(manage_events=True)
    async def event_cancel(self, interaction: discord.Interaction, event_id: int):
        db = get_db()
        event = next((e for e in db.data["events"] if e["event_id"] == event_id and e["guild_id"] == interaction.guild.id), None)
        
        if not event:
            return await interaction.response.send_message("❌ Event not found.", ephemeral=True)
            
        db.data["events"] = [e for e in db.data["events"] if e["event_id"] != event_id]
        db.data["event_rsvps"] = [r for r in db.data["event_rsvps"] if r["event_id"] != event_id]
        db.save()
        
        try:
            msg = await interaction.channel.fetch_message(event["message_id"])
            await msg.delete()
        except discord.NotFound:
            pass
            
        await interaction.response.send_message(f"✅ Event `{event_id}` has been cancelled.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Events(bot))
    bot.add_view(RSVPView())
