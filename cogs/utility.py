import discord
from discord.ext import commands
from discord import app_commands
import os
import datetime
import asyncio
import random

class TicketCloseButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger, custom_id="ticket_close_btn", emoji="❌")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.channel.name.startswith("ticket-"):
            return await interaction.response.send_message("This command can only be used in ticket channels.", ephemeral=True)
            
        await interaction.response.send_message("Closing ticket in 5 seconds...")
        await asyncio.sleep(5)
        await interaction.channel.delete(reason=f"Ticket closed by {interaction.user.name}")

class TicketCreateButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.primary, custom_id="ticket_create_btn", emoji="🎫")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        
        existing_channel = discord.utils.get(guild.channels, name=f"ticket-{interaction.user.name.lower()}")
        if existing_channel:
            return await interaction.response.send_message(f"You already have an open ticket: {existing_channel.mention}", ephemeral=True)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
        }
        
        for role in guild.roles:
            if role.permissions.manage_channels:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)

        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            try:
                category = await guild.create_category("Tickets")
            except Exception:
                category = None

        channel = await guild.create_text_channel(
            f"ticket-{interaction.user.name}",
            category=category,
            overwrites=overwrites,
            reason=f"Ticket created for {interaction.user.name}"
        )
        
        embed = discord.Embed(
            title="🎫 Support Ticket | Dion Corp",
            description=f"Welcome {interaction.user.mention}!\n\nPlease describe your issue and our support team will be with you shortly. To close this ticket, click the ❌ button below.",
            color=0x005A9C
        )
        await channel.send(embed=embed, view=TicketCloseButton())
        await interaction.response.send_message(f"Ticket created successfully! Please proceed to {channel.mention}", ephemeral=True)


class Utility(commands.Cog):
    """
    General utility, moderation, and support commands for Dion Corp.
    Manages temporary private voice channels, support tickets, and moderation.
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.temp_channels = {}

    @app_commands.command(name='setup_voice', description="Sets up the dynamic 'Join to Create' voice category and channel.")
    @app_commands.default_permissions(administrator=True)
    async def setup_voice(self, interaction: discord.Interaction):
        """Creates the category and channel for dynamic voice hubs."""
        guild = interaction.guild
        
        category = discord.utils.get(guild.categories, name="Dynamic Voice Hubs")
        if not category:
            category = await guild.create_category("Dynamic Voice Hubs")
            
        join_channel = discord.utils.get(guild.voice_channels, name="➕ Join to Create")
        if not join_channel:
            join_channel = await guild.create_voice_channel("➕ Join to Create", category=category)
            
        embed = discord.Embed(
            title="🎤 Dion Corp Dynamic Voice",
            description=f"Voice hub setup successfully! Users can join {join_channel.mention} to create their own private lounge.",
            color=0x005A9C
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """Manages dynamic voice channels creation and cleanup."""
        guild = member.guild
        
        if after.channel and after.channel.name == "➕ Join to Create":
            category = after.channel.category
            
            new_channel = await guild.create_voice_channel(
                name=f"🔊 {member.display_name}'s Lounge",
                category=category,
                reason=f"Dynamic voice hub created for {member.name}"
            )
            
            await new_channel.set_permissions(member, manage_channels=True, mute_members=True, deafen_members=True)
            await member.move_to(new_channel)
            self.temp_channels[new_channel.id] = new_channel

        if before.channel and before.channel.id in self.temp_channels:
            if len(before.channel.members) == 0:
                try:
                    await before.channel.delete(reason="Dynamic voice hub empty")
                    del self.temp_channels[before.channel.id]
                except discord.NotFound:
                    pass
                except Exception as e:
                    print(f"Failed to delete temp voice channel: {e}")

    @app_commands.command(name='lfg', description="Looking For Group - Tag a squad role to announce you're looking for gamers.")
    @app_commands.describe(
        game="The game you want to play.",
        role="The squad role you want to ping (optional).",
        details="Any extra details (e.g., 'need 2 more', 'ranked')."
    )
    async def lfg(self, interaction: discord.Interaction, game: str, role: discord.Role = None, details: str = "Let's play!"):
        """Allows users to ping a role for gaming."""
        role_mention = role.mention if role else "@here"
        
        embed = discord.Embed(
            title=f"🎮 LFG: {game}",
            description=f"**{interaction.user.mention}** is looking for players!\n\n**Details:** {details}",
            color=0x3498DB
        )
        embed.set_footer(text="Join them in a voice channel!")
        
        await interaction.response.send_message(f"Hey {role_mention}, who's down?", embed=embed)

    @app_commands.command(name='setup_tickets', description="Sets up the ticket creation panel in the current channel.")
    @app_commands.default_permissions(administrator=True)
    async def setup_tickets(self, interaction: discord.Interaction):
        """Sets up the ticket system."""
        embed = discord.Embed(
            title="📞 Dion Corp Support",
            description="Do you need assistance or have an inquiry?\n\nClick the **Create Ticket** button below to open a private channel with our support team.",
            color=0x005A9C
        )
        embed.set_footer(text="Dion Corp Customer Service")
        
        await interaction.channel.send(embed=embed, view=TicketCreateButton())
        await interaction.response.send_message("Ticket panel set up successfully.", ephemeral=True)

    @app_commands.command(name='close_ticket', description="Closes the current ticket channel.")
    @app_commands.default_permissions(manage_channels=True)
    async def close_ticket_cmd(self, interaction: discord.Interaction):
        """Closes a ticket manually via command."""
        if not interaction.channel.name.startswith("ticket-"):
            return await interaction.response.send_message("This command can only be used in ticket channels.", ephemeral=True)
            
        await interaction.response.send_message("Closing ticket in 5 seconds...")
        await asyncio.sleep(5)
        await interaction.channel.delete(reason=f"Ticket closed by {interaction.user.name} via command")

    @app_commands.command(name='clear', description="Deletes a specified number of messages from the channel.")
    @app_commands.default_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int = 5):
        """Deletes a specified number of messages from the channel."""
        await interaction.response.defer(ephemeral=True)
        purged = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f'🧹 Cleaned `{len(purged)}` messages from this sector.', ephemeral=True)

    @app_commands.command(name='alert', description="Broadcasts an engineered global alert to the channel.")
    @app_commands.default_permissions(administrator=True)
    async def alert(self, interaction: discord.Interaction, message: str):
        """Broadcasts an engineered global alert to the channel."""
        embed = discord.Embed(
            title="🚨 DION CORP | SYSTEM ANNOUNCEMENT",
            description=message,
            color=0x005A9C
        )
        embed.set_footer(text=f"Authorized by: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='changelog', description="Post a beautifully formatted bot changelog announcement.")
    @app_commands.default_permissions(administrator=True)
    async def changelog(self, interaction: discord.Interaction, version: str, changes: str, channel: discord.TextChannel = None):
        """Post a beautifully formatted bot changelog announcement."""
        target_channel = channel or interaction.channel
        change_items = [item.strip() for item in changes.split(';') if item.strip()]
        formatted_changes = "\n".join([f"• {item}" for item in change_items])

        embed = discord.Embed(
            title=f"🚀 Dion Corp System Update: {version}",
            color=0x005A9C
        )
        embed.add_field(name="What's New:", value=formatted_changes or "No details provided.", inline=False)
        embed.set_footer(text=f"Updates compiled by: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        
        try:
            await target_channel.send(embed=embed)
            await interaction.response.send_message(f"✅ Changelog posted successfully to {target_channel.mention}!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to send message: {e}", ephemeral=True)

    @app_commands.command(name='lock', description="Locks the current text channel, stopping members from typing.")
    @app_commands.default_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        """Locks the current text channel."""
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
        embed = discord.Embed(
            description="🔒 **Sector Lockdown Initiated.** Text operations suspended.",
            color=0x005A9C
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='unlock', description="Unlocks the text channel, restoring standard operational permissions.")
    @app_commands.default_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        """Unlocks the text channel."""
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
        embed = discord.Embed(
            description="🔓 **Sector Unlocked.** Operations fully restored.",
            color=0x005A9C
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='timeout', description="Time out a user for a specified duration.")
    @app_commands.default_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, duration_minutes: int, reason: str = "No reason provided."):
        """Times out a user."""
        try:
            duration = datetime.timedelta(minutes=duration_minutes)
            await member.timeout(duration, reason=reason)
            embed = discord.Embed(
                title="⏱️ Timeout Issued | Dion Corp Security",
                description=f"**Target:** {member.mention}\n**Duration:** `{duration_minutes} minutes`\n**Reason:** {reason}",
                color=0x005A9C
            )
            embed.set_footer(text=f"Authorized by: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Error: I do not have permission to time out this user.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {e}", ephemeral=True)

    @app_commands.command(name='kick', description="Kicks a user from the server.")
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
        """Kicks a user."""
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="👢 Kick Issued | Dion Corp Security",
                description=f"**Target:** {member.mention}\n**Reason:** {reason}",
                color=0x005A9C
            )
            embed.set_footer(text=f"Authorized by: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Error: I do not have permission to kick this user.", ephemeral=True)

    @app_commands.command(name='ban', description="Bans a user from the server.")
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
        """Bans a user."""
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="🔨 Ban Issued | Dion Corp Security",
                description=f"**Target:** {member.mention}\n**Reason:** {reason}",
                color=0x005A9C
            )
            embed.set_footer(text=f"Authorized by: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Error: I do not have permission to ban this user.", ephemeral=True)

    @app_commands.command(name='add_role', description="Assign a role to a user.")
    @app_commands.default_permissions(manage_roles=True)
    async def add_role(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        """Adds a role to a user."""
        try:
            await member.add_roles(role)
            await interaction.response.send_message(f"✅ Added {role.mention} to {member.mention}.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Error: I do not have permission to assign this role. Check my role hierarchy.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {e}", ephemeral=True)

    @app_commands.command(name='remove_role', description="Remove a role from a user.")
    @app_commands.default_permissions(manage_roles=True)
    async def remove_role(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        """Removes a role from a user."""
        try:
            await member.remove_roles(role)
            await interaction.response.send_message(f"✅ Removed {role.mention} from {member.mention}.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Error: I do not have permission to remove this role.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {e}", ephemeral=True)

    @app_commands.command(name='add_level', description="Manually increase a user's level.")
    @app_commands.default_permissions(administrator=True)
    async def add_level(self, interaction: discord.Interaction, member: discord.Member, amount: int = 1):
        """Adds levels to a user's profile."""
        engine_cog = self.bot.get_cog("Engine")
        if not engine_cog:
            return await interaction.response.send_message("❌ Error: Engine cog not loaded.", ephemeral=True)
            
        uid = str(member.id)
        engine_cog.users.setdefault(uid, {"xp": 0, "level": 1, "coins": 0, "last_message": 0})
        engine_cog.users[uid]["level"] += amount
        
        await interaction.response.send_message(f"✅ Added {amount} level(s) to {member.mention}. They are now Level {engine_cog.users[uid]['level']}.")

    @app_commands.command(name='remove_level', description="Manually decrease a user's level.")
    @app_commands.default_permissions(administrator=True)
    async def remove_level(self, interaction: discord.Interaction, member: discord.Member, amount: int = 1):
        """Removes levels from a user's profile."""
        engine_cog = self.bot.get_cog("Engine")
        if not engine_cog:
            return await interaction.response.send_message("❌ Error: Engine cog not loaded.", ephemeral=True)
            
        uid = str(member.id)
        engine_cog.users.setdefault(uid, {"xp": 0, "level": 1, "coins": 0, "last_message": 0})
        
        engine_cog.users[uid]["level"] = max(1, engine_cog.users[uid]["level"] - amount)
        await interaction.response.send_message(f"✅ Removed {amount} level(s) from {member.mention}. They are now Level {engine_cog.users[uid]['level']}.")

    @app_commands.command(name='add_xp', description="Manually grant XP to a user.")
    @app_commands.default_permissions(administrator=True)
    async def add_xp(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        """Adds XP to a user's profile."""
        engine_cog = self.bot.get_cog("Engine")
        if not engine_cog:
            return await interaction.response.send_message("❌ Error: Engine cog not loaded.", ephemeral=True)
            
        uid = str(member.id)
        engine_cog.users.setdefault(uid, {"xp": 0, "level": 1, "coins": 0, "last_message": 0})
        engine_cog.users[uid]["xp"] += amount
        
        current_level = engine_cog.users[uid]["level"]
        xp_needed = engine_cog.get_xp_for_level(current_level)
        if engine_cog.users[uid]["xp"] >= xp_needed:
            engine_cog.users[uid]["xp"] -= xp_needed
            engine_cog.users[uid]["level"] += 1
            await interaction.channel.send(f"🎉 **{member.mention}** leveled up to **Level {engine_cog.users[uid]['level']}**!")
            
        await interaction.response.send_message(f"✅ Added {amount} XP to {member.mention}.", ephemeral=True)

    @app_commands.command(name='remove_xp', description="Manually remove XP from a user.")
    @app_commands.default_permissions(administrator=True)
    async def remove_xp(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        """Removes XP from a user's profile."""
        engine_cog = self.bot.get_cog("Engine")
        if not engine_cog:
            return await interaction.response.send_message("❌ Error: Engine cog not loaded.", ephemeral=True)
            
        uid = str(member.id)
        engine_cog.users.setdefault(uid, {"xp": 0, "level": 1, "coins": 0, "last_message": 0})
        
        engine_cog.users[uid]["xp"] = max(0, engine_cog.users[uid]["xp"] - amount)
        await interaction.response.send_message(f"✅ Removed {amount} XP from {member.mention}.", ephemeral=True)

    @app_commands.command(name='giveaway', description="Starts a giveaway in the current channel.")
    @app_commands.default_permissions(manage_events=True)
    @app_commands.describe(
        prize="The prize to be won.",
        duration_minutes="How long the giveaway should last in minutes.",
        winners_count="Number of winners to select."
    )
    async def giveaway(self, interaction: discord.Interaction, prize: str, duration_minutes: int, winners_count: int = 1):
        """Starts a giveaway."""
        if duration_minutes <= 0:
            return await interaction.response.send_message("Duration must be at least 1 minute.", ephemeral=True)
            
        end_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=duration_minutes)
        end_timestamp = int(end_time.timestamp())

        embed = discord.Embed(
            title="🎉 Giveaway Initiated | Dion Corp",
            description=f"**Prize:** {prize}\n**Ends:** <t:{end_timestamp}:R>\n**Hosted by:** {interaction.user.mention}",
            color=0x005A9C
        )
        embed.set_footer(text=f"{winners_count} Winner(s) | React with 🎉 to enter!")
        
        await interaction.response.send_message("Giveaway starting...", ephemeral=True)
        message = await interaction.channel.send(embed=embed)
        await message.add_reaction("🎉")

        await asyncio.sleep(duration_minutes * 60)

        try:
            message = await interaction.channel.fetch_message(message.id)
        except discord.NotFound:
            return

        users = []
        for reaction in message.reactions:
            if str(reaction.emoji) == "🎉":
                async for user in reaction.users():
                    if not user.bot:
                        users.append(user)

        if len(users) == 0:
            embed.description = f"**Prize:** {prize}\n**Ended:** <t:{end_timestamp}:R>\n**Hosted by:** {interaction.user.mention}\n\n*No valid entries.*"
            await message.edit(embed=embed)
            await interaction.channel.send(f"Nobody entered the giveaway for **{prize}**.")
            return

        winners = random.sample(users, min(winners_count, len(users)))
        winner_mentions = ", ".join(w.mention for w in winners)

        embed.description = f"**Prize:** {prize}\n**Ended:** <t:{end_timestamp}:R>\n**Hosted by:** {interaction.user.mention}\n\n**Winner(s):** {winner_mentions}"
        embed.color = 0x2ECC71
        await message.edit(embed=embed)

        await interaction.channel.send(f"🎉 Congratulations {winner_mentions}! You won **{prize}**!")

    def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            return interaction.response.send_message("🛑 **Access Denied.** Your security clearance is insufficient for this command.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Utility(bot))
    bot.add_view(TicketCreateButton())
    bot.add_view(TicketCloseButton())
