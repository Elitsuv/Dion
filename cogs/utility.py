import discord
from discord.ext import commands
from discord import app_commands

class Utility(commands.Cog):
    """General utility commands and systems for Dion Corp."""
    def __init__(self, bot):
        self.bot = bot
        # Dictionary to track temporary private voice channels created
        self.temp_channels = {}

    @app_commands.command(name='setup_voice', description="Sets up the dynamic 'Join to Create' voice category and channel.")
    @app_commands.default_permissions(administrator=True)
    async def setup_voice(self, interaction: discord.Interaction):
        """Creates the category and channel for dynamic voice hubs."""
        guild = interaction.guild
        
        # Check if it already exists
        category = discord.utils.get(guild.categories, name="Dynamic Voice Hubs")
        if not category:
            category = await guild.create_category("Dynamic Voice Hubs")
            
        join_channel = discord.utils.get(guild.voice_channels, name="➕ Join to Create")
        if not join_channel:
            join_channel = await guild.create_voice_channel("➕ Join to Create", category=category)
            
        embed = discord.Embed(
            title="🎤 Dion Corp Dynamic Voice",
            description=f"Voice hub setup successfully! Users can join {join_channel.mention} to create their own private lounge.",
            color=0x005A9C
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guild = member.guild
        
        # Check if the user joined the "Join to Create" channel
        if after.channel and after.channel.name == "➕ Join to Create":
            category = after.channel.category
            
            # Create a new voice channel for the user
            new_channel = await guild.create_voice_channel(
                name=f"🔊 {member.display_name}'s Lounge",
                category=category,
                reason=f"Dynamic voice hub created for {member.name}"
            )
            
            # Give the user permission to manage their channel
            await new_channel.set_permissions(member, manage_channels=True, mute_members=True, deafen_members=True)
            
            # Move the user into the new channel
            await member.move_to(new_channel)
            
            # Track the channel
            self.temp_channels[new_channel.id] = new_channel

        # Check if a user left a tracked temporary channel
        if before.channel and before.channel.id in self.temp_channels:
            # If the channel is now empty, delete it
            if len(before.channel.members) == 0:
                try:
                    await before.channel.delete(reason="Dynamic voice hub empty")
                    del self.temp_channels[before.channel.id]
                except discord.NotFound:
                    pass
                except Exception as e:
                    print(f"Failed to delete temp voice channel: {e}")

async def setup(bot):
    await bot.add_cog(Utility(bot))
