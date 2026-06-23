import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configure intents
intents = discord.Intents.default()
# intents.members = True  # Disabled due to missing privileged intent


class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents, help_command=None)

    async def setup_hook(self):
        """Dynamically loads all modules inside the cogs folder."""
        print("🔗 Initializing extensions...")
        # Explicitly loading cogs to avoid file system race conditions
        extensions = ['cogs.admin', 'cogs.engine', 'cogs.games', 'cogs.chatbot', 'cogs.utility', 'cogs.help']
        for ext in extensions:
            try:
                await self.load_extension(ext)
                print(f"✅ Successfully loaded: {ext}")
            except Exception as e:
                print(f"❌ Failed to load {ext}: {e}")
        
        print("🔄 Syncing command tree...")
        try:
            synced = await self.tree.sync()
            print(f"✅ Synced {len(synced)} command(s).")
        except Exception as e:
            print(f"❌ Failed to sync command tree: {e}")

    async def on_ready(self):
        print(f'🚀 System online. Logged in as: {self.user}')
        print(f'📡 Connected to local machine node.')
        # Set a professional presence status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing, 
                name="Dion Corp | v1.0.3"
            )
        )

bot = DiscordBot()

if __name__ == '__main__':
    if not TOKEN:
        raise ValueError("CRITICAL: DISCORD_TOKEN variable is missing in .env file.")
    bot.run(TOKEN)