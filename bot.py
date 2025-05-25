from src.config import get_bot_config, TOKEN
from src.message_handler import process_message

# Initialize bot
bot = get_bot_config()

@bot.event
async def on_ready():
    print(f'{bot.user} đã sẵn sàng!')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Process message and send response
    response = process_message(message.content, message.author)
    await message.channel.send(response)

# Run the bot
try:
    bot.run(TOKEN)
except Exception as e:
    print(f"Lỗi khi khởi động bot: {str(e)}")