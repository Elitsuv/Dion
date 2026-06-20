import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='help', description="Shows all available commands for the bot.")
    async def help_command(self, interaction: discord.Interaction):
        """Displays an all-in-one help menu."""
        embed = discord.Embed(
            title="Dion Bot - Help Menu",
            description="Here are all the available commands you can use:",
            color=0xFFB347 # Light Orange theme
        )
        
        # General / User Commands
        embed.add_field(
            name="🎮 Fun & Predictions", 
            value="`/guess` - Play a 3x3 emoji guessing game!\n`/nlp_predict <query>` - Use NLP to predict World Cup match outcomes.\n`/predict <team_acs> <enemy_acs>` - Predict win probability based on stats.\n`/matrix <size> <elements>` - Calculate the determinant of a matrix.",
            inline=False
        )
        
        # Admin Commands
        embed.add_field(
            name="🛡️ Admin Commands", 
            value="`/clear <amount>` - Delete a set number of messages.\n`/lock` - Locks the current channel.\n`/unlock` - Unlocks the current channel.\n`/alert <message>` - Broadcast a system announcement.",
            inline=False
        )
        
        embed.set_footer(text="Requested by " + interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
