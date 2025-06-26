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
        print(f"DEBUG: Bot is ready! Connected as {self.user}")
        print(f"DEBUG: Bot is in {len(self.guilds)} guilds")
        for guild in self.guilds:
            print(f"DEBUG: Guild: {guild.name} (ID: {guild.id})")
        print(f"DEBUG: Command prefix: {self.command_prefix}")
        print(f"DEBUG: Loaded commands: {[cmd.name for cmd in self.commands]}")

    async def on_message(self, message) -> None:
        """Called when a message is received"""
        if message.author == self.user:
            return
            
        print(f"DEBUG: Message received from {message.author}: '{message.content}'")
        
        # Check if message starts with command prefix
        if message.content.startswith(self.command_prefix):
            print(f"DEBUG: Message starts with command prefix '{self.command_prefix}'")
        
        # Process commands
        await self.process_commands(message)
