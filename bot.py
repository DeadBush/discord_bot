import logging
from src.config import get_bot_config, TOKEN
from src.message_handler import process_message
import discord

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot with reconnect enabled
bot = get_bot_config()

@bot.event
async def on_ready():
    logger.info(f'{bot.user} đã sẵn sàng phục vụ!')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    # Chỉ phản hồi khi tin nhắn bắt đầu bằng '!thong'
    if message.content.startswith('!thong'):
        # Lấy nội dung sau '!thong'
        prompt = message.content[len('!thong'):].strip()
        user_name = message.author.display_name
        try:
            # Process message and send response (now async)
            print(f"Processing message from {user_name}: {prompt}")
            response = await process_message(prompt, user_name)
            await message.channel.send(response)
        except Exception as e:
            logger.error(f"Lỗi khi xử lý tin nhắn: {str(e)}")

@bot.event
async def on_error(event, *args, **kwargs):
    logger.error(f"Lỗi trong event {event}: {str(args)} - {str(kwargs)}")

@bot.event
async def on_disconnect():
    logger.warning("Bot đã mất kết nối từ Discord")

# Run the bot with auto-reconnect
while True:
    try:
        logger.info("Đang kết nối tới Discord...")
        bot.run(TOKEN)
    except discord.errors.ConnectionClosed:
        logger.warning("Mất kết nối. Đang thử kết nối lại...")
        continue
    except Exception as e:
        logger.error(f"Lỗi không mong đợi: {str(e)}")
        break