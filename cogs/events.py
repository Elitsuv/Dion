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
        
        event = db.get_event_by_message(message_id)
        if not event:
            return await interaction.response.send_message("❌ This event is no longer active in the database.", ephemeral=True)
            
        event_id = event["event_id"]
        
        db.set_rsvp(event_id, user_id, status)
        
        rsvps = db.get_rsvps(event_id)
        counts = {"attending": 0, "maybe": 0, "not_coming": 0}
        for r in rsvps:
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
        await interaction.followup.send(f"Your RSVP has been recorded as: **{status.replace('_', ' ').title()}**.", ephemeral=True)

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
        self.active_timers = {}

    async def cog_load(self):
        # Schedule the event recovery task
        self.bot.loop.create_task(self.recover_events())

    async def recover_events(self):
        await self.bot.wait_until_ready()
        db = get_db()
        all_events = db.get_events()
        now = datetime.utcnow()
        for e in all_events:
            event_id = e["event_id"]
            trigger_time = datetime.utcfromtimestamp(int(e["event_time"]))
            delay = (trigger_time - now).total_seconds()
            
            # Retrieve or fetch channel
            channel = self.bot.get_channel(e["channel_id"])
            if not channel:
                try:
                    channel = await self.bot.fetch_channel(e["channel_id"])
                except discord.HTTPException:
                    # Channel no longer exists, clean up event
                    db.remove_event(event_id)
                    continue

            if delay <= 0:
                if abs(delay) < 300:  # Within 5 minutes, run immediately
                    self.bot.loop.create_task(self.event_timer(channel, e["message_id"], 0, e["title"]))
                else:
                    db.remove_event(event_id)
            else:
                self.active_timers[event_id] = self.bot.loop.create_task(
                    self.event_timer(channel, e["message_id"], delay, e["title"])
                )

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
        try:
            await asyncio.sleep(delay)
        except asyncio.CancelledError:
            return
        
        db = get_db()
        event = db.get_event_by_message(message_id)
        if not event:
            return
            
        event_id = event["event_id"]
        rsvps = db.get_rsvps(event_id)
        attendees = [r["user_id"] for r in rsvps if r["status"] == "attending"]
        
        db.remove_event(event_id)
        if event_id in self.active_timers:
            del self.active_timers[event_id]
        
        mentions = " ".join([f"<@{uid}>" for uid in attendees])
        if not mentions:
            mentions = "No one RSVP'd 'Attending'."
            
        try:
            await channel.send(f"🔔 **Event Starting:** {title}!\n{mentions}")
        except discord.HTTPException:
            pass

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
        
        db.add_event(event_id, interaction.guild.id, interaction.user.id, title, description, timestamp, msg.id, interaction.channel.id)
        
        delay = (trigger_time - datetime.utcnow()).total_seconds()
        if delay > 0:
            self.active_timers[event_id] = self.bot.loop.create_task(
                self.event_timer(interaction.channel, msg.id, delay, title)
            )

    @app_commands.command(name='event_list', description="View upcoming events in this server.")
    async def event_list(self, interaction: discord.Interaction):
        db = get_db()
        guild_events = db.get_guild_events(interaction.guild.id)[-10:]
        
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
        event = db.get_event(event_id)
        
        if not event or event["guild_id"] != interaction.guild.id:
            return await interaction.response.send_message("❌ Event not found.", ephemeral=True)
            
        db.remove_event(event_id)
        
        if event_id in self.active_timers:
            self.active_timers[event_id].cancel()
            del self.active_timers[event_id]
        
        try:
            msg = await interaction.channel.fetch_message(event["message_id"])
            await msg.delete()
        except discord.NotFound:
            pass
            
        await interaction.response.send_message(f"✅ Event `{event_id}` has been cancelled.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Events(bot))
    bot.add_view(RSVPView())
