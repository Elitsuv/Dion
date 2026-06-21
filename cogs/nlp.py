import discord
from discord.ext import commands
from discord import app_commands
import numpy as np

class NLP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='fwc_predict', description="Predicts Football World Cup matches.")
    @app_commands.describe(team_a="First team name", team_b="Second team name")
    async def fwc_predict(self, interaction: discord.Interaction, team_a: str, team_b: str):
        """Predicts the winner between two teams."""
        
        team_a = team_a.strip().title()
        team_b = team_b.strip().title()

        # Simulate "Engine" prediction logic by creating a pseudo-ACS based on team name hashes
        # This provides a deterministic "prediction" for any given matchup
        hash_a = sum(ord(c) for c in team_a) % 100 + 150  # Score between 150 and 250
        hash_b = sum(ord(c) for c in team_b) % 100 + 150

        x1 = hash_a / 400.0
        x2 = hash_b / 400.0
        inputs = np.array([x1, x2])

        # Using similar weights to the engine cog
        weights = np.array([4.5, -4.5])
        bias = 0.0

        z = np.dot(inputs, weights) + bias
        probability = 1 / (1 + np.exp(-z))
        win_percentage_a = round(probability * 100, 2)
        win_percentage_b = round(100 - win_percentage_a, 2)

        # Determine winner
        if win_percentage_a > win_percentage_b:
            prediction_text = f"🏆 **{team_a}** is predicted to win against {team_b}!"
        elif win_percentage_b > win_percentage_a:
            prediction_text = f"🏆 **{team_b}** is predicted to win against {team_a}!"
        else:
            prediction_text = f"⚖️ It's a dead heat between {team_a} and {team_b}!"

        embed = discord.Embed(
            title="🌐 FWC Prediction Engine",
            description=f"Matchup: **{team_a} vs {team_b}**",
            color=0xFFB347
        )
        embed.add_field(name="Prediction", value=prediction_text, inline=False)
        embed.add_field(
            name="Win Probabilities", 
            value=f"{team_a}: `{win_percentage_a}%`\n{team_b}: `{win_percentage_b}%`", 
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(NLP(bot))
