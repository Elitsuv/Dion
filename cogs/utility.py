import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from datetime import datetime, timedelta
import sqlite3

from utils.embeds import DionEmbed
from utils.db import get_connection

class Utility(commands.Cog):
    """
    General utility commands for Dion Corp.
    Contains remind, poll, userinfo, and serverstats.
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.check_reminders())

    async def check_reminders(self):
        """Background task to check for due reminders."""
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            conn = get_connection()
            cursor = conn.cursor()
            now_str = datetime.utcnow().isoformat()
            
            cursor.execute("SELECT reminder_id, user_id, reminder_text FROM reminders WHERE trigger_time <= ?", (now_str,))
            due_reminders = cursor.fetchall()
            
            for r_id, u_id, text in due_reminders:
                user = self.bot.get_user(u_id)
                if user:
                    embed = DionEmbed(
                        title="Reminder",
                        description=f"You asked me to remind you about: **{text}**"
                    )
                    try:
                        await user.send(embed=embed)
                    except discord.Forbidden:
                        pass # User has DMs closed
                
                cursor.execute("DELETE FROM reminders WHERE reminder_id = ?", (r_id,))
            
            conn.commit()
            conn.close()
            await asyncio.sleep(30) # Check every 30 seconds

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

    @app_commands.command(name='remind', description="Set a reminder (e.g., '2h Start Mock Test')")
    @app_commands.describe(
        duration="Duration (e.g., 2h, 30m, 1d)",
        task="What to remind you about"
    )
    async def remind(self, interaction: discord.Interaction, duration: str, task: str):
        try:
            trigger_time = self.parse_time(duration)
        except ValueError as e:
            return await interaction.response.send_message(f"❌ {e}", ephemeral=True)
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reminders (user_id, reminder_text, trigger_time) VALUES (?, ?, ?)",
            (interaction.user.id, task, trigger_time.isoformat())
        )
        conn.commit()
        conn.close()
        
        timestamp = int(trigger_time.timestamp())
        embed = DionEmbed(
            title="Reminder Set",
            description=f"I will remind you about **{task}** <t:{timestamp}:R>."
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='poll', description="Quick poll creation")
    @app_commands.describe(
        question="The poll question",
        options="Comma separated options (max 10). Leave empty for Yes/No."
    )
    async def poll(self, interaction: discord.Interaction, question: str, options: str = None):
        embed = DionEmbed(title="Poll", description=f"**{question}**")
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        
        if not options:
            embed.set_footer(text="React with 👍 or 👎")
            await interaction.response.send_message("Poll created!", ephemeral=True)
            msg = await interaction.channel.send(embed=embed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
        else:
            opt_list = [o.strip() for o in options.split(',')]
            if len(opt_list) > 10:
                return await interaction.response.send_message("❌ Maximum 10 options allowed.", ephemeral=True)
                
            emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
            desc_lines = [f"**{question}**\n"]
            for idx, opt in enumerate(opt_list):
                desc_lines.append(f"{emojis[idx]} {opt}")
                
            embed.description = "\n".join(desc_lines)
            embed.set_footer(text="React to vote!")
            
            await interaction.response.send_message("Poll created!", ephemeral=True)
            msg = await interaction.channel.send(embed=embed)
            for i in range(len(opt_list)):
                await msg.add_reaction(emojis[i])

    @app_commands.command(name='userinfo', description="Display basic information about a user")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        
        embed = DionEmbed(title=f"User Info: {member.name}")
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Account Created", value=f"<t:{int(member.created_at.timestamp())}:D>", inline=True)
        embed.add_field(name="Joined Server", value=f"<t:{int(member.joined_at.timestamp())}:D>", inline=True)
        
        roles = [r.mention for r in member.roles if r.name != "@everyone"]
        roles_str = " ".join(roles) if roles else "None"
        if len(roles_str) > 1024:
            roles_str = "Too many roles to display."
        embed.add_field(name="Roles", value=roles_str, inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='serverstats', description="Display server statistics")
    async def serverstats(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = DionEmbed(title=f"Server Stats: {guild.name}")
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
            
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Created", value=f"<t:{int(guild.created_at.timestamp())}:D>", inline=True)
        embed.add_field(name="Members", value=str(guild.member_count), inline=True)
        
        channels = len(guild.text_channels) + len(guild.voice_channels)
        embed.add_field(name="Channels", value=str(channels), inline=True)
        embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="Boost Level", value=str(guild.premium_tier), inline=True)
        
        await interaction.response.send_message(embed=embed)


    def get_config(self, guild_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT setup_channel_id, category_id FROM temp_voice_config WHERE guild_id = ?", (guild_id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def get_temp_channel(self, channel_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT owner_id FROM active_temp_channels WHERE channel_id = ?", (channel_id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def set_temp_channel(self, channel_id, owner_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO active_temp_channels (channel_id, owner_id) VALUES (?, ?)", (channel_id, owner_id))
        conn.commit()
        conn.close()
        
    def remove_temp_channel(self, channel_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM active_temp_channels WHERE channel_id = ?", (channel_id,))
        conn.commit()
        conn.close()

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
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO temp_voice_config (guild_id, setup_channel_id, category_id) VALUES (?, ?, ?)",
            (guild.id, join_channel.id, category.id)
        )
        conn.commit()
        conn.close()
            
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
                return # Category was deleted manually

            new_channel = await guild.create_voice_channel(
                name=f"🔊 {member.display_name}'s Room",
                category=category,
                reason=f"Temp voice channel for {member.name}"
            )
            
            # Give owner permissions
            await new_channel.set_permissions(member, manage_channels=True, mute_members=True, deafen_members=True, move_members=True)
            self.set_temp_channel(new_channel.id, member.id)
            
            # Move the member
            try:
                await member.move_to(new_channel)
            except discord.HTTPException:
                # If moving failed (they left voice quickly), delete the channel
                await new_channel.delete()
                self.remove_temp_channel(new_channel.id)
                return

        # User left a channel
        if before.channel:
            temp_channel_data = self.get_temp_channel(before.channel.id)
            if temp_channel_data:
                # If channel is now empty
                if len(before.channel.members) == 0:
                    try:
                        await before.channel.delete(reason="Temp voice channel empty")
                    except discord.NotFound:
                        pass
                    finally:
                        self.remove_temp_channel(before.channel.id)
                else:
                    # Give ownership to the first remaining member if the owner left
                    owner_id = temp_channel_data[0]
                    if member.id == owner_id:
                        new_owner = before.channel.members[0]
                        self.set_temp_channel(before.channel.id, new_owner.id)
                        await before.channel.set_permissions(new_owner, manage_channels=True, mute_members=True, deafen_members=True, move_members=True)
                        await before.channel.set_permissions(member, overwrite=None)
                        await before.channel.edit(name=f"🔊 {new_owner.display_name}'s Room")

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


async def setup(bot):
    await bot.add_cog(Utility(bot))
