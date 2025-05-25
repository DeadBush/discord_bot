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
    return discord.Client(intents=intents) 