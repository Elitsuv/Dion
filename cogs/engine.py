import discord
from discord.ext import commands
from discord import app_commands
import numpy as np

class Engine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='predict', description="Predicts match win probability using a basic neural network forward pass.")
    async def predict(self, interaction: discord.Interaction, team_acs: float, enemy_acs: float):
        """Predicts match win probability using a basic neural network forward pass."""
        x1 = team_acs / 400.0
        x2 = enemy_acs / 400.0
        inputs = np.array([x1, x2])

        weights = np.array([4.5, -4.5])
        bias = 0.0

        z = np.dot(inputs, weights) + bias
        probability = 1 / (1 + np.exp(-z))
        win_percentage = round(probability * 100, 2)

        embed = discord.Embed(
            title="🧠 Dion Network Prediction",
            description=f"Analysis complete for {interaction.user.mention}.",
            color=0xFFB347
        )
        embed.add_field(name="Inputs Processed", value=f"Team ACS: `{team_acs}`\nEnemy ACS: `{enemy_acs}`", inline=False)
        embed.add_field(name="Calculated Win Probability", value=f"**{win_percentage}%**", inline=False)
        
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
            title="📊 Linear Algebra Engine",
            color=0xFFB347
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
