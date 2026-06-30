import discord
from datetime import datetime, timezone

class DionEmbed(discord.Embed):
    """
    Base embed class for Dion to ensure consistent branding.
    Color is white.
    """
    def __init__(self, title=None, description=None, **kwargs):
        color = kwargs.pop('color', 0xFFFFFF)
        super().__init__(
            title=title,
            description=description,
            color=color, # White branding by default
            **kwargs
        )
        self.timestamp = datetime.now(timezone.utc)
