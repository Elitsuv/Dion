"""
Help module for the Dion Discord Bot.
Provides an organized, central command directory.
"""

import discord
from discord.ext import commands
from discord import app_commands

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
        embed = discord.Embed(
            title="🏢 Dion Corp | Central Command Directory",
            description="Welcome to the Dion Corp bot terminal. Below is the list of authorized operations:",
            color=0x005A9C
        )
        
        embed.add_field(
            name="🎮 Entertainment & Progress", 
            value="`/tictactoe <opponent>` - Play Tic-Tac-Toe.\n`/set_country_chain <channel> <mode>` - Setup word chain.\n`/profile [user]` - View Dion Corp employee profile & level.",
            inline=False
        )
        
        embed.add_field(
            name="🎫 User Engagement & Voice",
            value="`/giveaway <prize> <duration> [winners]` - Start a server giveaway.\n`/setup_tickets` - Initialize the ticket support portal.\n`/setup_voice` - Setup Dynamic 'Join to Create' voice hubs.\n`/lfg <game> [role] [details]` - Ping for players.",
            inline=False
        )
        
        embed.add_field(
            name="🛡️ Administration & Security", 
            value="`/clear <amount>` - Bulk delete messages.\n`/lock` / `/unlock` - Control channel text operations.\n`/timeout`, `/kick`, `/ban` - Access control tools.\n`/add_role`, `/remove_role` - Assign roles.\n`/add_level`, `/remove_level`, `/add_xp`, `/remove_xp` - Control employee progression.\n`/alert`, `/changelog` - Global announcements.",
            inline=False
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Authorized Request by: {interaction.user.display_name} | Dion Corp IT Division", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    """Adds the Help cog to the bot instance."""
    await bot.add_cog(Help(bot))
