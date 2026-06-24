import unittest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from main import DiscordBot
from discord import Intents

class TestDionBot(unittest.TestCase):
    def setUp(self):
        self.bot = DiscordBot()
        self.bot.load_extension = AsyncMock()
        self.bot.tree.sync = AsyncMock(return_value=[1, 2, 3])

    def test_intents_configured(self):
        """Test if the correct intents are initialized."""
        self.assertEqual(self.bot.intents, Intents.default())

    def test_bot_command_prefix(self):
        """Test if the bot command prefix is set correctly."""
        self.assertEqual(self.bot.command_prefix, '!')

    def test_setup_hook_loads_extensions(self):
        """Test if the setup_hook correctly loads the extensions."""
        # Using a synchronous event loop for testing async setup_hook
        async def run_setup():
            await self.bot.setup_hook()

        asyncio.run(run_setup())
        
        expected_extensions = ['cogs.engine', 'cogs.games', 'cogs.utility', 'cogs.help']
        self.assertEqual(self.bot.load_extension.call_count, len(expected_extensions))
        
        for ext in expected_extensions:
            self.bot.load_extension.assert_any_call(ext)

    def test_setup_hook_syncs_tree(self):
         """Test if the setup_hook syncs the slash command tree."""
         async def run_setup():
             await self.bot.setup_hook()
             
         asyncio.run(run_setup())
         self.bot.tree.sync.assert_called_once()

if __name__ == '__main__':
    unittest.main()
