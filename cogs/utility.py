import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from datetime import datetime, timedelta

from utils.embeds import DionEmbed
from utils.db import get_db

class Utility(commands.Cog):
    """
    General utility commands for Dion Corp.
    Contains temporary voice channel system.
    """
    
    def __init__(self, bot):
        self.bot = bot

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
