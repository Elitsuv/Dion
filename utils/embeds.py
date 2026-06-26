import discord
from datetime import datetime, timezone

class DionEmbed(discord.Embed):
    """
    Base embed class for Dion to ensure consistent branding.
    Color is white, and includes the otter 🦦 emoji optionally.
    """
    def __init__(self, title=None, description=None, **kwargs):
        super().__init__(
            title=f"🦦 {title}" if title else None,
            description=description,
            color=0xFFFFFF, # White branding
            **kwargs
        )
        self.timestamp = datetime.now(timezone.utc)
