import discord
from discord.ext import commands
import logging


class TTSBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True

        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self) -> None:
        """Called when the bot is starting up"""
        logging.info("Bot is starting up...")

    async def on_ready(self) -> None:
        """Called when the bot is ready"""
        logging.info(f"{self.user} has connected to Discord!")
