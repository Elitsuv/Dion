"""
Main entry point for the Dion Discord Bot.
Handles bot initialization, configuration, and startup.
"""

import os
import asyncio
import discord
from discord.ext import commands
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
            
        self.loop.create_task(self.live_stats_task())

    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.application_command:
            db = get_db()
            user_id = str(interaction.user.id)
            db.data["command_usage"][user_id] = db.data.get("command_usage", {}).get(user_id, 0) + 1
            db.data["user_last_active"][user_id] = discord.utils.utcnow().strftime("%H:%M:%S")
            db.save()

    async def live_stats_task(self):
        await self.wait_until_ready()
        while not self.is_closed():
            os.system('cls' if os.name == 'nt' else 'clear')
            db = get_db()
            print("="*60)
            print(f"{'User':<25} | {'Commands Used':<15} | {'Last Active':<15}")
            print("-" * 60)
            
            usage = db.data.get("command_usage", {})
            last_active = db.data.get("user_last_active", {})
            
            sorted_users = sorted(usage.items(), key=lambda x: x[1], reverse=True)
            
            if not sorted_users:
                print(f"{'No activity yet.':<25} | {'-':<15} | {'-':<15}")
            else:
                for uid_str, count in sorted_users[:15]:
                    user = self.get_user(int(uid_str))
                    username = user.name if user else f"Unknown ({uid_str})"
                    if len(username) > 23:
                        username = username[:20] + "..."
                    active_time = last_active.get(uid_str, "Unknown")
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