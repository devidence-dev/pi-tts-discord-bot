from discord.ext import commands
import discord
import asyncio
import os
from bot.tts.engine import TTSEngine


class TTSCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.tts_engine = TTSEngine()
        self.allowed_users = self._load_allowed_users()

    def _load_allowed_users(self) -> set:
        """Load allowed user IDs from environment"""
        user_ids_str = os.getenv("ALLOWED_USER_IDS", "")
        if not user_ids_str:
            return set()

        user_ids = []
        for uid in user_ids_str.split(","):
            uid = uid.strip()
            if uid.isdigit():
                user_ids.append(int(uid))

        return set(user_ids)

    def _is_authorized(self, user_id: int) -> bool:
        """Check if user is authorized to use the bot"""
        return not self.allowed_users or user_id in self.allowed_users

    @commands.command(name="tts")
    async def text_to_speech(self, ctx, *, text: str):
        """Convert text to speech"""
        if not self._is_authorized(ctx.author.id):
            await ctx.send("❌ You are not authorized to use this bot.")
            return

        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel!")
            return

        channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            await channel.connect()
        elif ctx.voice_client.channel != channel:
            await ctx.voice_client.move_to(channel)

        await ctx.send(f"Converting to speech: `{text}`")

        # Generate audio
        audio_path = self.tts_engine.synthesize(text)

        # Play audio
        audio_source = discord.FFmpegPCMAudio(audio_path)
        ctx.voice_client.play(audio_source)

        # Wait for playback to finish
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)

        # Cleanup
        self.tts_engine.cleanup_file(audio_path)

    @commands.command(name="join")
    async def join_voice(self, ctx):
        """Join the voice channel"""
        if not self._is_authorized(ctx.author.id):
            await ctx.send("❌ You are not authorized to use this bot.")
            return

        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel!")
            return

        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()
            await ctx.send(f"Joined {channel.name}")
        else:
            await ctx.send("Already connected to a voice channel!")

    @commands.command(name="leave")
    async def leave_voice(self, ctx):
        """Leave the voice channel"""
        if not self._is_authorized(ctx.author.id):
            await ctx.send("❌ You are not authorized to use this bot.")
            return

        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected from voice channel")
        else:
            await ctx.send("Not connected to any voice channel!")


async def setup(bot):
    await bot.add_cog(TTSCommands(bot))
