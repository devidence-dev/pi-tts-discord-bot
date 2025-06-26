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
        print(f"DEBUG: TTS command received from user {ctx.author.id}: '{text}'")
        
        if not self._is_authorized(ctx.author.id):
            print(f"DEBUG: User {ctx.author.id} not authorized")
            await ctx.send("❌ You are not authorized to use this bot.")
            return

        print(f"DEBUG: User authorized, checking voice channel")
        if not ctx.author.voice:
            print(f"DEBUG: User not in voice channel")
            await ctx.send("You need to be in a voice channel!")
            return

        channel = ctx.author.voice.channel
        print(f"DEBUG: User in voice channel: {channel.name}")

        if ctx.voice_client is None:
            print(f"DEBUG: Bot not connected, connecting to voice channel")
            await channel.connect()
        elif ctx.voice_client.channel != channel:
            print(f"DEBUG: Bot in different channel, moving")
            await ctx.voice_client.move_to(channel)

        print(f"DEBUG: Bot connected to voice, starting TTS processing")

        await ctx.send(f"Converting to speech: `{text}`")

        # Generate audio in a separate thread to avoid blocking
        loop = asyncio.get_event_loop()
        audio_path = await loop.run_in_executor(None, self.tts_engine.synthesize, text)
        
        print(f"DEBUG: Audio file generated at: {audio_path}")
        
        # Check if file exists and get size
        import os
        if os.path.exists(audio_path):
            file_size = os.path.getsize(audio_path)
            print(f"DEBUG: Audio file exists, size: {file_size} bytes")
        else:
            print(f"DEBUG: Audio file does not exist!")
            await ctx.send("❌ Failed to generate audio file")
            return

        # Play audio
        try:
            audio_source = discord.FFmpegPCMAudio(audio_path)
            print(f"DEBUG: Created FFmpegPCMAudio source")
            
            if ctx.voice_client:
                print(f"DEBUG: Voice client exists, starting playback")
                ctx.voice_client.play(audio_source)
                print(f"DEBUG: Audio playback started")
                
                # Wait for playback to finish
                while ctx.voice_client.is_playing():
                    print(f"DEBUG: Audio is playing...")
                    await asyncio.sleep(1)
                    
                print(f"DEBUG: Audio playback finished")
            else:
                print(f"DEBUG: No voice client available")
                await ctx.send("❌ Not connected to voice channel")
                
        except Exception as e:
            print(f"DEBUG: Error during audio playback: {e}")
            await ctx.send(f"❌ Error playing audio: {e}")

        # Cleanup
        self.tts_engine.cleanup_file(audio_path)
        print(f"DEBUG: Audio file cleaned up")

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


def setup(bot):
    bot.add_cog(TTSCommands(bot))
