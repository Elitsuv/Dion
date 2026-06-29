"""
Main entry point for the Dion Discord Bot.
Handles bot initialization, configuration, and startup.
"""

import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from utils.db import get_db

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
# intents.members = True  # Disabled due to missing privileged intent

class DiscordBot(commands.Bot):
    """
    The main bot class inheriting from commands.Bot.
    Responsible for setting up extensions and syncing the command tree.
    """
    
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents, help_command=None)

    async def setup_hook(self):
        """
        Dynamically loads all modules inside the cogs folder.
        Extensions are loaded explicitly to avoid file system race conditions.
        After loading extensions, the slash command tree is synced globally.
        """
        print("Initializing extensions...")
        extensions = [
            'cogs.utility', 
            'cogs.moderation', 
            'cogs.events',
            'cogs.alerts',
            'cogs.help'
        ]
        for ext in extensions:
            try:
                await self.load_extension(ext)
                print(f"Successfully loaded: {ext}")
            except Exception as e:
                print(f"Failed to load {ext}: {e}")
        
        # Register global slash command error handler
        @self.tree.error
        async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
            from utils.embeds import DionEmbed
            embed = DionEmbed(
                title="Error Encountered",
                description="An error occurred while executing this command."
            )
            embed.color = 0xFF0000 # Red for errors
            
            if isinstance(error, app_commands.MissingPermissions):
                embed.description = f"❌ You do not have the required permissions to use this command.\nMissing: `{', '.join(error.missing_permissions)}`"
            elif isinstance(error, app_commands.BotMissingPermissions):
                embed.description = f"❌ The bot is missing permissions to perform this command.\nMissing: `{', '.join(error.missing_permissions)}`"
            elif isinstance(error, app_commands.CommandOnCooldown):
                embed.description = f"⏱️ This command is on cooldown. Try again in `{error.retry_after:.2f}s`."
            else:
                embed.description = f"❌ An unexpected error occurred: `{error}`"
                print(f"Command Error: {error}")
            
            try:
                if interaction.response.is_done():
                    await interaction.followup.send(embed=embed, ephemeral=True)
                else:
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            except Exception as e:
                print(f"Failed to respond to error: {e}")

        print("Syncing command tree...")
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s).")
        except Exception as e:
            print(f"Failed to sync command tree: {e}")
            
        self.loop.create_task(self.live_stats_task())

    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.application_command:
            db = get_db()
            user_id = str(interaction.user.id)
            active_time = discord.utils.utcnow().strftime("%H:%M:%S")
            db.record_command_usage(user_id, active_time)

    async def live_stats_task(self):
        await self.wait_until_ready()
        while not self.is_closed():
            os.system('cls' if os.name == 'nt' else 'clear')
            db = get_db()
            print("="*60)
            print(f"{'User':<25} | {'Commands Used':<15} | {'Last Active':<15}")
            print("-" * 60)
            
            stats = db.get_command_usage_stats()
            
            if not stats:
                print(f"{'No activity yet.':<25} | {'-':<15} | {'-':<15}")
            else:
                for row in stats:
                    uid_str = row["user_id"]
                    count = row["command_count"]
                    active_time = row["last_active"]
                    
                    user = self.get_user(int(uid_str))
                    username = user.name if user else f"Unknown ({uid_str})"
                    if len(username) > 23:
                        username = username[:20] + "..."
                    print(f"{username:<25} | {count:<15} | {active_time:<15}")
                    
            print("="*60)
            print("Bot is running... Press Ctrl+C to exit.")
            await asyncio.sleep(10)

    async def on_ready(self):
        """Called when the bot is fully ready and connected to Discord."""
        print(f'System online. Logged in as: {self.user}')
        print(f'Connected to local machine node.')
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing, 
                name="Dion Corp | v2.1.0"
            )
        )

bot = DiscordBot()

if __name__ == '__main__':
    if not TOKEN:
        raise ValueError("CRITICAL: DISCORD_TOKEN variable is missing in .env file.")
    bot.run(TOKEN)