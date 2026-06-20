import discord
from discord.ext import commands
from discord import app_commands
import re
import random
import numpy as np

class NLP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='nlp_predict', description="Predicts World Cup matches using natural language.")
    @app_commands.describe(query="E.g., Predict who will win between Brazil and Germany")
    async def nlp_predict(self, interaction: discord.Interaction, query: str):
        """Extracts teams from a natural language query and predicts the winner."""
        # Simple NLP entity extraction using Regex for common query formats
        # Matches formats like: "between TeamA and TeamB", "TeamA vs TeamB"
        pattern = r"(?:between|match|vs\.?|predict)[\s]+([A-Z][a-zA-Z\s]+?)[\s]+(?:and|vs\.?)[\s]+([A-Z][a-zA-Z\s]+)"
        
        match = re.search(pattern, query, re.IGNORECASE)
        
        if not match:
            # Fallback if the pattern doesn't match
            await interaction.response.send_message(
                "❌ **NLP Parsing Failed:** I couldn't understand the teams in your query. Try something like: `Predict the match between Argentina and France`",
                ephemeral=True
            )
            return
            
        team_a = match.group(1).strip().title()
        team_b = match.group(2).strip().title()

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
            title="🌐 NLP World Cup Prediction Engine",
            description=f"Query parsed: `{query}`",
            color=0xFFB347
        )
        embed.add_field(name="Entities Extracted", value=f"Team 1: **{team_a}**\nTeam 2: **{team_b}**", inline=False)
        embed.add_field(name="Prediction", value=prediction_text, inline=False)
        embed.add_field(
            name="Win Probabilities", 
            value=f"{team_a}: `{win_percentage_a}%`\n{team_b}: `{win_percentage_b}%`", 
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(NLP(bot))
