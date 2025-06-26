import asyncio
import logging
import os
from dotenv import load_dotenv
from bot.client import TTSBot

# Load environment variables
load_dotenv()


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    bot = TTSBot()

    # Load commands
    bot.load_extension("bot.commands")

    # Get token from environment variable
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("DISCORD_TOKEN environment variable is required")

    await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
