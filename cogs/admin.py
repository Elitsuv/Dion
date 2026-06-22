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

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger, custom_id="ticket_close_btn", emoji="🔒")
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
            description=f"Welcome {interaction.user.mention}!\n\nPlease describe your issue and our support team will be with you shortly. To close this ticket, click the button below.",
            color=0x005A9C
        )
        await channel.send(embed=embed, view=TicketCloseButton())
        await interaction.response.send_message(f"Ticket created successfully! Please proceed to {channel.mention}", ephemeral=True)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------
    # CORE ADMIN COMMANDS
    # -------------------
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
    @app_commands.describe(
        version="The version number (e.g., v1.1.0)",
        changes="The changes list, use ';' to separate different items.",
        channel="Optional target channel. Uses CHANGELOG_CHANNEL_ID env var or current channel as fallback."
    )
    async def changelog(self, interaction: discord.Interaction, version: str, changes: str, channel: discord.TextChannel = None):
        """Post a beautifully formatted bot changelog announcement."""
        target_channel = channel
        if not target_channel:
            env_channel_id = os.getenv('CHANGELOG_CHANNEL_ID')
            if env_channel_id:
                try:
                    target_channel = self.bot.get_channel(int(env_channel_id))
                except ValueError:
                    pass
        if not target_channel:
            target_channel = interaction.channel

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
            await interaction.response.send_message(f"❌ Failed to send message to {target_channel.mention}: {e}", ephemeral=True)

    @app_commands.command(name='lock', description="Locks the current text channel, stopping members from typing.")
    @app_commands.default_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        """Locks the current text channel, stopping members from typing."""
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
        embed = discord.Embed(
            description="🔒 **Sector Lockdown Initiated.** Text operations suspended.",
            color=0x005A9C
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='unlock', description="Unlocks the text channel, restoring standard operational permissions.")
    @app_commands.default_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        """Unlocks the text channel, restoring standard operational permissions."""
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
        embed = discord.Embed(
            description="🔓 **Sector Unlocked.** Operations fully restored.",
            color=0x005A9C
        )
        await interaction.response.send_message(embed=embed)

    # -------------------
    # MODERATION COMMANDS
    # -------------------
    @app_commands.command(name='timeout', description="Time out a user for a specified duration.")
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.describe(
        member="The user to time out.",
        duration_minutes="Duration of the timeout in minutes.",
        reason="Reason for the timeout."
    )
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
            await interaction.response.send_message("❌ Error: I do not have permission to time out this user. Check my role hierarchy.", ephemeral=True)
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
            await interaction.response.send_message("❌ Error: I do not have permission to kick this user. Check my role hierarchy.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {e}", ephemeral=True)

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
            await interaction.response.send_message("❌ Error: I do not have permission to ban this user. Check my role hierarchy.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {e}", ephemeral=True)

    # -------------------
    # GIVEAWAY COMMANDS
    # -------------------
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

    # -------------------
    # TICKET SYSTEM
    # -------------------
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

    # -------------------
    # EVENTS
    # -------------------
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.system_channel
        if not channel:
            for c in member.guild.text_channels:
                if c.permissions_for(member.guild.me).send_messages and "welcome" in c.name.lower():
                    channel = c
                    break
            if not channel:
                for c in member.guild.text_channels:
                    if c.permissions_for(member.guild.me).send_messages:
                        channel = c
                        break

        if channel:
            embed = discord.Embed(
                title="🏢 Welcome to the Server | Dion Corp",
                description=f"Welcome, {member.mention}, to **{member.guild.name}**.\n\nWe are pleased to have you join our community. Please ensure you review the corporate guidelines and familiarize yourself with the available channels.",
                color=0x005A9C
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"Employee #{member.guild.member_count} | Dion Corp Human Resources")
            
            try:
                await channel.send(embed=embed)
            except discord.Forbidden:
                pass

    # -------------------
    # ERROR HANDLING
    # -------------------
    def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            return interaction.response.send_message("🛑 **Access Denied.** Your security clearance is insufficient for this command.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))
    bot.add_view(TicketCreateButton())
    bot.add_view(TicketCloseButton())
