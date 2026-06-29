"""
Help module for the Dion Discord Bot.
Provides an organized, central command directory.
"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import DionEmbed

class Help(commands.Cog):
    """
    Cog responsible for handling the dynamic help command.
    It provides a centralized directory of available commands 
    organized by categories.
    """
    
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='help', description="Displays the Dion Corp internal command directory.")
    async def help_command(self, interaction: discord.Interaction):
        """Displays a dynamic, all-in-one help menu."""
        embed = DionEmbed(
            title="Dion Corp | Central Command Directory",
            description="Welcome to the Dion Corp bot terminal. Below is the list of authorized operations:"
        )
        embed.color = 0x005A9C
        
        embed.add_field(
            name="🎤 Temporary Voice Channels", 
            value=(
                "`/vc_setup` - Sets up the voice channels category and creator channel.\n"
                "`/vc_lock` - Locks your temporary voice channel.\n"
                "`/vc_unlock` - Unlocks your temporary voice channel.\n"
                "`/vc_rename <name>` - Renames your voice channel.\n"
                "`/vc_limit <limit>` - Sets a user limit on your channel.\n"
                "`/vc_delete` - Deletes your temporary voice channel immediately."
            ),
            inline=False
        )
        
        embed.add_field(
            name="📅 Event Management",
            value=(
                "`/event_create <title> <description> <duration>` - Create a new event with RSVP buttons.\n"
                "`/event_list` - View upcoming events in the server.\n"
                "`/event_cancel <event_id>` - Cancel an event."
            ),
            inline=False
        )

        embed.add_field(
            name="🔔 Opt-in Alerts System",
            value=(
                "`/alert_create <name>` - Create a new alert topic and its role (Admin).\n"
                "`/alert_delete <name>` - Delete an alert topic and its role (Admin).\n"
                "`/alert_list` - List all available alert topics.\n"
                "`/alert_join <name>` - Subscribe to an alert topic.\n"
                "`/alert_leave <name>` - Unsubscribe from an alert topic.\n"
                "`/alert_send <name> <message>` - Send announcement pinging topic subscribers (Admin)."
            ),
            inline=False
        )
        
        embed.add_field(
            name="🛡️ Administration & Moderation", 
            value=(
                "`/warn <member> <reason>` - Warn a member.\n"
                "`/warnings <member>` - View warnings for a member.\n"
                "`/modlogs <member>` - View modlogs for a member.\n"
                "`/timeout <member> <minutes> [reason]` - Timeout a member.\n"
                "`/kick <member> [reason]` - Kick a member.\n"
                "`/ban <member> [reason]` - Ban a member.\n"
                "`/purge [amount]` - Delete a specified number of messages."
            ),
            inline=False
        )

        embed.add_field(
            name="🎭 Reaction Roles",
            value=(
                "`/reactionrole add <message_id> <emoji> <role>` - Bind a reaction role.\n"
                "`/reactionrole remove <message_id> <emoji>` - Remove a reaction role bind.\n"
                "`/reactionrole list` - List all active reaction role binds."
            ),
            inline=False
        )

        embed.add_field(
            name="📢 Professional Messaging",
            value=(
                "`/say <message> [title] [channel] [image_file] [image_url] [color] [as_embed]` - Send a styled message on behalf of the bot."
            ),
            inline=False
        )

        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Authorized Request by: {interaction.user.display_name} | Dion Corp IT Division", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    """Adds the Help cog to the bot instance."""
    await bot.add_cog(Help(bot))
