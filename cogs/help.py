"""
Help module for the Dion Discord Bot.
Provides an organized, central command directory.
"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import DionEmbed

class HelpDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Home / Overview", description="Main help menu", emoji="🏠", value="0"),
            discord.SelectOption(label="Voice Channels", description="Temporary voice channel commands", emoji="🎤", value="1"),
            discord.SelectOption(label="Events & Alerts", description="Scheduling and subscriber topics", emoji="📅", value="2"),
            discord.SelectOption(label="Moderation & Security", description="Admin warning and action commands", emoji="🛡️", value="3"),
            discord.SelectOption(label="Reaction Roles & Messaging", description="Custom messages and role setups", emoji="🎭", value="4"),
        ]
        super().__init__(placeholder="Select a category...", min_values=1, max_values=1, options=options, custom_id="help_select")

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        view.current_page = int(self.values[0])
        await view.update_message(interaction)

class HelpView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=180.0)
        self.interaction = interaction
        self.current_page = 0
        self.total_pages = 5
        self.add_item(HelpDropdown())
        
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        try:
            await self.interaction.edit_original_response(view=self)
        except Exception:
            pass

    def get_page_embed_and_file(self):
        file = discord.File("assets/dion.png", filename="dion.png")
        embed = DionEmbed(
            color=0x005A9C
        )
        embed.set_thumbnail(url="attachment://dion.png")
        embed.set_footer(
            text=f"Page {self.current_page + 1}/{self.total_pages} | Dion Corp IT Division",
            icon_url="attachment://dion.png"
        )

        if self.current_page == 0:
            embed.title = "Dion Corp | Central Command Directory"
            embed.description = (
                "Welcome to the Dion Corp bot terminal. Use the buttons below or the dropdown menu "
                "to navigate through authorized server operations.\n\n"
                "**Command Categories:**\n"
                "• **Page 2: 🎤 Temporary Voice Channels**\n"
                "• **Page 3: 📅 Event Management & Alerts**\n"
                "• **Page 4: 🛡️ Administration & Moderation**\n"
                "• **Page 5: 🎭 Reaction Roles & Messaging**"
            )
        elif self.current_page == 1:
            embed.title = "🎤 Temporary Voice Channels"
            embed.description = "Create and configure temporary voice channels that auto-delete when empty."
            embed.add_field(
                name="Setup & Lifetime",
                value=(
                    "| `/vc_setup` - Set up creation category and creator channel (Admin).\n"
                    "| `/vc_delete` - Instantly deletes your temporary voice channel."
                ),
                inline=False
            )
            embed.add_field(
                name="Channel Customization",
                value=(
                    "| `/vc_lock` - Locks your channel, preventing others from joining.\n"
                    "| `/vc_unlock` - Unlocks your channel.\n"
                    "| `/vc_rename <name>` - Renames your temporary voice channel.\n"
                    "| `/vc_limit <limit>` - Restricts maximum user count."
                ),
                inline=False
            )
        elif self.current_page == 2:
            embed.title = "📅 Events & Alerts"
            embed.description = "Coordinated scheduling and opt-in announcement roles."
            embed.add_field(
                name="Event Management",
                value=(
                    "| `/event_create <title> <description> <duration>` - Schedule a new event.\n"
                    "| `/event_list` - View upcoming events.\n"
                    "| `/event_cancel <id>` - Cancel an event."
                ),
                inline=False
            )
            embed.add_field(
                name="Alert Subscriptions",
                value=(
                    "| `/alert_create <name>` - Create alert topic & role (Admin).\n"
                    "| `/alert_delete <name>` - Delete alert topic & role (Admin).\n"
                    "| `/alert_list` - List all topics.\n"
                    "| `/alert_join <name>` - Subscribe to alerts.\n"
                    "| `/alert_leave <name>` - Unsubscribe from alerts.\n"
                    "| `/alert_send <name> <message>` - Ping all subscribers (Admin)."
                ),
                inline=False
            )
        elif self.current_page == 3:
            embed.title = "🛡️ Administration & Moderation"
            embed.description = "Keep your server safe and organized."
            embed.add_field(
                name="Warnings & Logs",
                value=(
                    "| `/warn <user> <reason>` - Warn a member.\n"
                    "| `/warnings <user>` (also `/modlogs`) - View warnings for a member."
                ),
                inline=False
            )
            embed.add_field(
                name="Moderation Actions",
                value=(
                    "| `/timeout <user> <minutes> [reason]` - Timeout a member.\n"
                    "| `/kick <user> [reason]` - Kick a member.\n"
                    "| `/ban <user> [reason]` - Ban a member.\n"
                    "| `/purge [amount]` - Purge recent messages."
                ),
                inline=False
            )
        elif self.current_page == 4:
            embed.title = "🎭 Reaction Roles & Messaging"
            embed.description = "Configure interactive roles and custom messages."
            embed.add_field(
                name="Reaction Roles",
                value=(
                    "| `/reactionrole add <message_id> <emoji> <role>` - Bind reaction role.\n"
                    "| `/reactionrole remove <message_id> <emoji>` - Remove bind.\n"
                    "| `/reactionrole list` - List active binds."
                ),
                inline=False
            )
            embed.add_field(
                name="Broadcasting",
                value=(
                    "| `/say <message> [title] [channel] [image_file] [image_url] [color] [as_embed]` - Broadcast styled messages."
                ),
                inline=False
            )

        return embed, file

    async def update_message(self, interaction: discord.Interaction):
        embed, file = self.get_page_embed_and_file()
        self.children[0].disabled = (self.current_page == 0)
        self.children[2].disabled = (self.current_page == self.total_pages - 1)
        await interaction.response.edit_message(embed=embed, attachments=[file], view=self)

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary, emoji="◀️", custom_id="help_prev")
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
        await self.update_message(interaction)

    @discord.ui.button(label="Help Menu", style=discord.ButtonStyle.primary, emoji="ℹ️", custom_id="help_home")
    async def home_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = 0
        await self.update_message(interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary, emoji="▶️", custom_id="help_next")
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
        await self.update_message(interaction)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, emoji="❌", custom_id="help_close")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.delete()
        except Exception:
            await interaction.response.send_message("Closed help menu.", ephemeral=True)

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
        view = HelpView(interaction)
        embed, file = view.get_page_embed_and_file()
        view.children[0].disabled = True
        await interaction.response.send_message(embed=embed, file=file, view=view)

async def setup(bot):
    """Adds the Help cog to the bot instance."""
    await bot.add_cog(Help(bot))
