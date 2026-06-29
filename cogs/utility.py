"""
General utility and system operations cog for Dion Corp.
Contains voice channel management, event coordination, alert notifications,
reaction role configuration, and professional announcement features.
All time operations are aligned to Indian Standard Time (IST).
"""

import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from datetime import datetime, timezone, timedelta

from utils.embeds import DionEmbed
from utils.db import get_db

# Indian Standard Time (IST) timezone representation
IST = timezone(timedelta(hours=5, minutes=30))

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


class Utility(commands.Cog):
    """
    Core Utility system. Manages Voice setup, Event RSVPs, Alert list subscriptions,
    Reaction Roles bindings, and professional messages.
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.active_timers = {}

    async def cog_load(self):
        # Schedule the event recovery task
        self.bot.loop.create_task(self.recover_events())

    # ==========================================
    # DATABASE & HELPER UTILITIES (Voice Channels)
    # ==========================================
    def get_config(self, guild_id):
        db = get_db()
        config = db.get_temp_voice_config(guild_id)
        if config:
            return (config["setup_channel_id"], config["category_id"])
        return None

    def get_temp_channel(self, channel_id):
        db = get_db()
        channel = db.get_active_temp_channel(channel_id)
        if channel:
            return (int(channel["owner_id"]),)
        return None

    def set_temp_channel(self, channel_id, owner_id):
        db = get_db()
        db.set_active_temp_channel(channel_id, owner_id)
        
    def remove_temp_channel(self, channel_id):
        db = get_db()
        db.remove_active_temp_channel(channel_id)

    def _is_owner(self, interaction: discord.Interaction):
        if not interaction.user.voice or not interaction.user.voice.channel:
            return False, "You are not in a voice channel."
        
        channel_id = interaction.user.voice.channel.id
        data = self.get_temp_channel(channel_id)
        if not data:
            return False, "You are not in a temporary voice channel."
        if data[0] != interaction.user.id and not interaction.user.guild_permissions.administrator:
            return False, "You don't own this temporary voice channel."
            
        return True, interaction.user.voice.channel

    # ==========================================
    # VOICE CHANNEL COMMANDS
    # ==========================================
    @app_commands.command(name='vc_setup', description="Sets up the temporary voice channels system.")
    @app_commands.default_permissions(administrator=True)
    async def vc_setup(self, interaction: discord.Interaction):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Voice Lounges")
        if not category:
            category = await guild.create_category("Voice Lounges")
            
        join_channel = discord.utils.get(guild.voice_channels, name="➕ Create Voice Channel", category=category)
        if not join_channel:
            join_channel = await guild.create_voice_channel("➕ Create Voice Channel", category=category)
            
        db = get_db()
        db.set_temp_voice_config(guild.id, join_channel.id, category.id)
            
        embed = DionEmbed(
            title="🎤 Voice Setup Complete",
            description=f"Users can now join {join_channel.mention} to automatically create their own temporary voice channel."
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guild = member.guild
        config = self.get_config(guild.id)
        if not config:
            return
            
        setup_channel_id, category_id = config
        
        # User joined the setup channel
        if after.channel and after.channel.id == setup_channel_id:
            category = guild.get_channel(category_id)
            if not category:
                return

            new_channel = await guild.create_voice_channel(
                name=f"🔊 {member.display_name}'s Room",
                category=category,
                reason=f"Temp voice channel for {member.name}"
            )
            
            await new_channel.set_permissions(member, manage_channels=True, mute_members=True, deafen_members=True, move_members=True)
            self.set_temp_channel(new_channel.id, member.id)
            
            try:
                await member.move_to(new_channel)
            except discord.HTTPException:
                await new_channel.delete()
                self.remove_temp_channel(new_channel.id)
                return

        # User left a channel
        if before.channel:
            temp_channel_data = self.get_temp_channel(before.channel.id)
            if temp_channel_data:
                if len(before.channel.members) == 0:
                    try:
                        await before.channel.delete(reason="Temp voice channel empty")
                    except discord.NotFound:
                        pass
                    finally:
                        self.remove_temp_channel(before.channel.id)
                else:
                    owner_id = temp_channel_data[0]
                    if member.id == owner_id:
                        new_owner = before.channel.members[0]
                        self.set_temp_channel(before.channel.id, new_owner.id)
                        await before.channel.set_permissions(new_owner, manage_channels=True, mute_members=True, deafen_members=True, move_members=True)
                        await before.channel.set_permissions(member, overwrite=None)
                        await before.channel.edit(name=f"🔊 {new_owner.display_name}'s Room")

    @app_commands.command(name='vc_lock', description="Locks your temporary voice channel.")
    async def vc_lock(self, interaction: discord.Interaction):
        is_owner, channel_or_err = self._is_owner(interaction)
        if not is_owner:
            return await interaction.response.send_message(f"❌ {channel_or_err}", ephemeral=True)
            
        await channel_or_err.set_permissions(interaction.guild.default_role, connect=False)
        await interaction.response.send_message("🔒 Your voice channel has been locked.", ephemeral=True)

    @app_commands.command(name='vc_unlock', description="Unlocks your temporary voice channel.")
    async def vc_unlock(self, interaction: discord.Interaction):
        is_owner, channel_or_err = self._is_owner(interaction)
        if not is_owner:
            return await interaction.response.send_message(f"❌ {channel_or_err}", ephemeral=True)
            
        await channel_or_err.set_permissions(interaction.guild.default_role, connect=True)
        await interaction.response.send_message("🔓 Your voice channel has been unlocked.", ephemeral=True)

    @app_commands.command(name='vc_rename', description="Renames your temporary voice channel.")
    async def vc_rename(self, interaction: discord.Interaction, name: str):
        is_owner, channel_or_err = self._is_owner(interaction)
        if not is_owner:
            return await interaction.response.send_message(f"❌ {channel_or_err}", ephemeral=True)
            
        await channel_or_err.edit(name=name)
        await interaction.response.send_message(f"✅ Renamed to **{name}**.", ephemeral=True)

    @app_commands.command(name='vc_limit', description="Sets a user limit for your voice channel (0 for no limit).")
    async def vc_limit(self, interaction: discord.Interaction, limit: app_commands.Range[int, 0, 99]):
        is_owner, channel_or_err = self._is_owner(interaction)
        if not is_owner:
            return await interaction.response.send_message(f"❌ {channel_or_err}", ephemeral=True)
            
        await channel_or_err.edit(user_limit=limit)
        limit_text = f"{limit} users" if limit > 0 else "Unlimited"
        await interaction.response.send_message(f"✅ User limit set to **{limit_text}**.", ephemeral=True)

    @app_commands.command(name='vc_delete', description="Deletes your temporary voice channel immediately.")
    async def vc_delete(self, interaction: discord.Interaction):
        is_owner, channel_or_err = self._is_owner(interaction)
        if not is_owner:
            return await interaction.response.send_message(f"❌ {channel_or_err}", ephemeral=True)
            
        await interaction.response.send_message("🗑️ Deleting channel...", ephemeral=True)
        try:
            await channel_or_err.delete()
        except discord.NotFound:
            pass
        finally:
            self.remove_temp_channel(channel_or_err.id)

    # ==========================================
    # EVENT COORDINATION METHODS (IST)
    # ==========================================
    async def recover_events(self):
        await self.bot.wait_until_ready()
        db = get_db()
        all_events = db.get_events()
        now = datetime.now(IST)
        for e in all_events:
            event_id = e["event_id"]
            trigger_time = datetime.fromtimestamp(int(e["event_time"]), tz=IST)
            delay = (trigger_time - now).total_seconds()
            
            channel = self.bot.get_channel(e["channel_id"])
            if not channel:
                try:
                    channel = await self.bot.fetch_channel(e["channel_id"])
                except discord.HTTPException:
                    db.remove_event(event_id)
                    continue

            if delay <= 0:
                if abs(delay) < 300:
                    self.bot.loop.create_task(self.event_timer(channel, e["message_id"], 0, e["title"]))
                else:
                    db.remove_event(event_id)
            else:
                self.active_timers[event_id] = self.bot.loop.create_task(
                    self.event_timer(channel, e["message_id"], delay, e["title"])
                )

    def parse_time(self, time_str: str) -> datetime:
        time_str = time_str.lower()
        now = datetime.now(IST)
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
        event_id = int(datetime.now(IST).timestamp() * 1000)
        db.add_event(event_id, interaction.guild.id, interaction.user.id, title, description, timestamp, msg.id, interaction.channel.id)
        
        delay = (trigger_time - datetime.now(IST)).total_seconds()
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

    # ==========================================
    # ALERT SYSTEM COMMANDS
    # ==========================================
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
            await interaction.followup.send(f"✅ Successfully subscribed to **{name_clean}**!", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("❌ I do not have permission to manage roles for you.", ephemeral=True)

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
            await interaction.followup.send("❌ I do not have permission to manage roles for you.", ephemeral=True)

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
        await interaction.channel.send(content=role.mention, embed=embed)
        await interaction.followup.send(f"✅ Announcement sent to {role.mention}.", ephemeral=True)

    # ==========================================
    # REACTION ROLE COMMANDS & LISTENERS
    # ==========================================
    reaction_group = app_commands.Group(name="reactionrole", description="Manage reaction roles.")

    @reaction_group.command(name="add", description="Binds a role to a message reaction.")
    @app_commands.default_permissions(manage_roles=True)
    async def rx_add(self, interaction: discord.Interaction, message_id: str, emoji: str, role: discord.Role):
        db = get_db()
        try:
            msg_id = int(message_id)
        except ValueError:
            return await interaction.response.send_message("❌ Invalid Message ID. Must be a numeric string.", ephemeral=True)

        db.add_reaction_role(interaction.guild.id, msg_id, emoji, role.id)
        embed = DionEmbed(
            title="✅ Reaction Role Added",
            description=f"Bound {role.mention} to {emoji} on message ID `{msg_id}`."
        )
        await interaction.response.send_message(embed=embed)

    @reaction_group.command(name="remove", description="Removes a reaction role bind.")
    @app_commands.default_permissions(manage_roles=True)
    async def rx_remove(self, interaction: discord.Interaction, message_id: str, emoji: str):
        db = get_db()
        try:
            msg_id = int(message_id)
        except ValueError:
            return await interaction.response.send_message("❌ Invalid Message ID. Must be a numeric string.", ephemeral=True)

        db.remove_reaction_role(interaction.guild.id, msg_id, emoji)
        embed = DionEmbed(
            title="🗑️ Reaction Role Removed",
            description=f"Removed the {emoji} reaction role mapping from message ID `{msg_id}`."
        )
        await interaction.response.send_message(embed=embed)

    @reaction_group.command(name="list", description="Lists all reaction role binds.")
    @app_commands.default_permissions(manage_roles=True)
    async def rx_list(self, interaction: discord.Interaction):
        db = get_db()
        binds = db.get_all_reaction_roles(interaction.guild.id)
        if not binds:
            return await interaction.response.send_message("❌ No reaction roles configured on this server.", ephemeral=True)
            
        embed = DionEmbed(title="Reaction Role Mappings")
        for b in binds:
            msg_id = b["message_id"]
            emoji = b["emoji"]
            role_id = int(b["role_id"])
            role = interaction.guild.get_role(role_id)
            role_mention = role.mention if role else f"Deleted Role (ID: {role_id})"
            embed.add_field(
                name=f"Message ID: {msg_id}",
                value=f"Emoji: {emoji} ➔ Role: {role_mention}",
                inline=False
            )
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return

        db = get_db()
        emoji_str = str(payload.emoji)
        mapping = db.get_reaction_role(payload.guild_id, payload.message_id, emoji_str)
        if not mapping:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        role = guild.get_role(int(mapping["role_id"]))
        if not role:
            return

        member = payload.member
        if not member:
            try:
                member = await guild.fetch_member(payload.user_id)
            except discord.HTTPException:
                return

        try:
            await member.add_roles(role, reason="Reaction Role Assignment")
        except discord.Forbidden:
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        db = get_db()
        emoji_str = str(payload.emoji)
        mapping = db.get_reaction_role(payload.guild_id, payload.message_id, emoji_str)
        if not mapping:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        role = guild.get_role(int(mapping["role_id"]))
        if not role:
            return

        try:
            member = await guild.fetch_member(payload.user_id)
        except discord.HTTPException:
            return

        try:
            await member.remove_roles(role, reason="Reaction Role Removal")
        except discord.Forbidden:
            pass

    # ==========================================
    # PROFESSIONAL MESSAGING (/SAY COMMAND)
    # ==========================================
    @app_commands.command(name="say", description="Sends a message to a channel on behalf of the bot.")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(
        message="The body content of the message",
        title="Optional title for the embed",
        channel="The target channel (defaults to current channel)",
        image_file="Upload an image to attach or embed",
        image_url="A web URL pointing to an image",
        color="Hex color code (e.g., #00FF00)",
        as_embed="Whether to send the message styled inside an embed (default: True)"
    )
    async def say(
        self,
        interaction: discord.Interaction,
        message: str,
        title: str = None,
        channel: discord.TextChannel = None,
        image_file: discord.Attachment = None,
        image_url: str = None,
        color: str = None,
        as_embed: bool = True
    ):
        target_channel = channel or interaction.channel
        permissions = target_channel.permissions_for(interaction.guild.me)
        if not permissions.send_messages:
            return await interaction.response.send_message(f"❌ I do not have permission to send messages in {target_channel.mention}.", ephemeral=True)

        embed_color = 0xFFFFFF
        if color:
            color_clean = color.lstrip('#')
            try:
                embed_color = int(color_clean, 16)
            except ValueError:
                return await interaction.response.send_message("❌ Invalid color format. Please use a hex code.", ephemeral=True)

        resolved_image_url = image_file.url if image_file else image_url

        if as_embed:
            embed = DionEmbed(title=title, description=message)
            embed.color = embed_color
            embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
            if resolved_image_url:
                embed.set_image(url=resolved_image_url)
            await target_channel.send(embed=embed)
        else:
            if image_file:
                file = await image_file.to_file()
                await target_channel.send(content=message, file=file)
            elif image_url:
                await target_channel.send(content=f"{message}\n{image_url}")
            else:
                await target_channel.send(content=message)

        await interaction.response.send_message(f"✅ Message sent to {target_channel.mention} successfully.", ephemeral=True)


async def setup(bot):
    """Adds the consolidated Utility cog to the bot instance and loads the persistent RSVP view."""
    await bot.add_cog(Utility(bot))
    bot.add_view(RSVPView())
