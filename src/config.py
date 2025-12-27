import discord
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot configuration
def get_bot_config():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.presences = True  # Required for detecting game activities
    intents.members = True    # Required for presence updates
    return discord.Client(intents=intents) 