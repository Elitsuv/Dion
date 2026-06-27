"""
Main entry point for the Dion Discord Bot.
Handles bot initialization, configuration, and startup.
"""

import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

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
            'cogs.events'
        ]
        for ext in extensions:
            try:
                await self.load_extension(ext)
                print(f"Successfully loaded: {ext}")
            except Exception as e:
                print(f"Failed to load {ext}: {e}")
        
        print("Syncing command tree...")
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s).")
        except Exception as e:
            print(f"Failed to sync command tree: {e}")

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