import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='help', description="Displays the Dion Corp internal command directory.")
    async def help_command(self, interaction: discord.Interaction):
        """Displays a dynamic, all-in-one help menu."""
        embed = discord.Embed(
            title="🏢 Dion Corp | Central Command Directory",
            description="Welcome to the Dion Corp bot terminal. Below is the list of authorized operations:",
            color=0x005A9C # Corporate Blue theme
        )
        
        # We can dynamically pull commands from the bot's tree if we want, 
        # but for clean categorization, we define them manually here.
        # This prevents internal/owner-only commands from leaking to regular users.
        
        embed.add_field(
            name="🎮 Entertainment & AI", 
            value="`/tictactoe <opponent>` - Play Tic-Tac-Toe.\n`/set_country_chain <channel> <mode>` - Setup word chain.\n`/fifa_predict <team_a> <team_b>` - AI FIFA match prediction.\n`/matrix <size> <elements>` - Linear algebra determinant engine.\n`/profile [user]` - View Dion Corp employee profile & level.",
            inline=False
        )
        
        embed.add_field(
            name="🎫 User Engagement",
            value="`/giveaway <prize> <duration> [winners]` - Start a server giveaway.\n`/setup_tickets` - Initialize the ticket support portal.",
            inline=False
        )
        
        embed.add_field(
            name="🛡️ Administration & Security", 
            value="`/clear <amount>` - Bulk delete messages.\n`/lock` / `/unlock` - Control channel text operations.\n`/timeout <user> <duration> [reason]` - Suspend employee chat access.\n`/kick <user>` / `/ban <user>` - Terminate employee access.\n`/alert <message>` - Broadcast system-wide alert.\n`/changelog <version> <changes>` - Post formatted release notes.",
            inline=False
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Authorized Request by: {interaction.user.display_name} | Dion Corp IT Division", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
