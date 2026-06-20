import discord
from discord.ext import commands
from discord import app_commands
import random

class EmojiGameView(discord.ui.View):
    def __init__(self, target_row: int, target_col: int):
        super().__init__(timeout=60)
        self.target_row = target_row
        self.target_col = target_col
        self.game_over = False

        # Build a 3x3 grid
        for row in range(3):
            for col in range(3):
                self.add_item(EmojiButton(row, col))

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        self.game_over = True
        # Note: In a real bot, we might want to edit the original message on timeout,
        # but for simplicity we'll just stop processing clicks.

class EmojiButton(discord.ui.Button):
    def __init__(self, row: int, col: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="❓", row=row)
        self.grid_row = row
        self.grid_col = col

    async def callback(self, interaction: discord.Interaction):
        view: EmojiGameView = self.view
        
        if view.game_over:
            return

        if self.grid_row == view.target_row and self.grid_col == view.target_col:
            self.label = "🏆"
            self.style = discord.ButtonStyle.success
            view.game_over = True
            content = f"🎉 **{interaction.user.mention} found the prize!** You win!"
            # Disable all buttons and reveal the prize
            for child in view.children:
                child.disabled = True
                if child.grid_row == view.target_row and child.grid_col == view.target_col:
                    child.label = "🏆"
                    child.style = discord.ButtonStyle.success
                else:
                    child.label = "❌"
                    child.style = discord.ButtonStyle.danger
        else:
            self.label = "❌"
            self.style = discord.ButtonStyle.danger
            self.disabled = True
            content = f"**{interaction.user.mention} guessed wrong!** Keep searching!"

        await interaction.response.edit_message(content=content, view=view)


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='guess', description="Start a 3x3 emoji guessing game!")
    async def guess(self, interaction: discord.Interaction):
        """Starts a 3x3 emoji guessing game."""
        target_row = random.randint(0, 2)
        target_col = random.randint(0, 2)
        
        view = EmojiGameView(target_row, target_col)
        await interaction.response.send_message(
            content="🎲 **Find the hidden prize!** Click a button below to guess.",
            view=view
        )

async def setup(bot):
    await bot.add_cog(Games(bot))
