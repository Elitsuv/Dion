import discord
from discord.ext import commands
from discord import app_commands
import numpy as np
import json
import os
import time
import random

DATA_FILE = "users.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Engine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users = load_data()

    def get_xp_for_level(self, level):
        return int(100 * (level ** 1.5))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        user_id = str(message.author.id)
        if user_id not in self.users:
            self.users[user_id] = {"xp": 0, "level": 1, "coins": 0, "last_message": 0}

        if "coins" not in self.users[user_id]:
            self.users[user_id]["coins"] = 0

        current_time = time.time()
        # 60 seconds cooldown for XP
        if current_time - self.users[user_id].get("last_message", 0) > 60:
            xp_gain = random.randint(15, 25)
            self.users[user_id]["xp"] += xp_gain
            self.users[user_id]["last_message"] = current_time

            # Level up check
            current_level = self.users[user_id]["level"]
            xp_needed = self.get_xp_for_level(current_level)

            if self.users[user_id]["xp"] >= xp_needed:
                self.users[user_id]["xp"] -= xp_needed
                self.users[user_id]["level"] += 1
                try:
                    await message.channel.send(f"🎉 **{message.author.mention}** leveled up to **Level {self.users[user_id]['level']}**!")
                except discord.HTTPException:
                    pass

            save_data(self.users)

    @app_commands.command(name='profile', description="Shows your level, XP, and coins.")
    async def profile(self, interaction: discord.Interaction, member: discord.Member = None):
        """Shows the user's level, XP, coins, and progress."""
        target = member or interaction.user
        if target.bot:
            await interaction.response.send_message("Bots do not have profiles.", ephemeral=True)
            return

        user_id = str(target.id)
        user_data = self.users.get(user_id, {"xp": 0, "level": 1, "coins": 0})
        
        current_level = user_data.get("level", 1)
        current_xp = user_data.get("xp", 0)
        coins = user_data.get("coins", 0)
        xp_needed = self.get_xp_for_level(current_level)

        embed = discord.Embed(title=f"👤 Dion Corp Employee: {target.display_name}", color=0x005A9C)
        embed.set_thumbnail(url=target.display_avatar.url if target.display_avatar else target.default_avatar.url)
        embed.add_field(name="Level", value=f"`{current_level}`", inline=True)
        embed.add_field(name="Coins", value=f"🪙 `{coins}`", inline=True)
        embed.add_field(name="XP", value=f"`{current_xp} / {xp_needed}`", inline=True)

        progress = int((current_xp / xp_needed) * 10) if xp_needed > 0 else 0
        bar = "🟩" * progress + "⬜" * (10 - progress)
        embed.add_field(name="Progress to Next Level", value=bar, inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='matrix', description="Computes the determinant of a square matrix. Provide elements as space-separated numbers.")
    async def matrix(self, interaction: discord.Interaction, rows_cols: int, elements: str):
        """Computes the determinant of a square matrix."""
        try:
            element_list = [float(e) for e in elements.split()]
        except ValueError:
            return await interaction.response.send_message("❌ Error: Please provide valid numbers for elements, separated by spaces.", ephemeral=True)

        if len(element_list) != rows_cols ** 2:
            await interaction.response.send_message(f"❌ Error: Expected {rows_cols**2} elements for a {rows_cols}x{rows_cols} matrix, got {len(element_list)}.", ephemeral=True)
            return

        matrix_np = np.array(element_list).reshape(rows_cols, rows_cols)
        det = np.linalg.det(matrix_np)
        
        embed = discord.Embed(
            title="📊 Dion Corp | Linear Algebra Engine",
            color=0x005A9C
        )
        embed.add_field(name="Input Matrix", value=f"```\n{matrix_np}\n```", inline=False)
        embed.add_field(name=r"Determinant ($\Delta$)", value=f"`{round(det, 4)}`", inline=False)
        
        if abs(det) > 1e-9:
            embed.add_field(name="Status", value="System is non-singular. A unique solution exists.", inline=False)
        else:
            embed.add_field(name="Status", value="Matrix is singular (infinite or no solutions).", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Engine(bot))
