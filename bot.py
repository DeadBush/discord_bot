import logging
import asyncio
from src.config import get_bot_config, TOKEN
from src.message_handler import process_message
from src.riot_tracker import riot_tracker
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
    
    # Start Valorant match monitoring
    if not riot_tracker.is_running:
        # Set notification channel to the first available text channel
        # You can customize this or set it via command
        for guild in bot.guilds:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    riot_tracker.set_notification_channel(channel.id)
                    logger.info(f"Set notification channel to: {channel.name} ({channel.id})")
                    break
            if riot_tracker.notification_channel_id:
                break
        
        # Start monitoring in background
        asyncio.create_task(riot_tracker.start_monitoring(bot, check_interval=30))
        logger.info("Valorant match monitoring started")

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Ignore empty messages
    if not message.content or message.content.strip() == "":
        return
    
    # Handle Valorant tracking commands
    content = message.content.strip()
    
    # Command: !track valorant <riot_name> <riot_tag>
    if content.startswith("!track valorant"):
        try:
            parts = content.split()
            if len(parts) >= 4:
                riot_name = parts[2]
                riot_tag = parts[3]
                discord_user_id = str(message.author.id)
                
                riot_tracker.add_tracked_player(discord_user_id, riot_name, riot_tag)
                await message.channel.send(
                    f"✅ Đã thêm {riot_name}#{riot_tag} vào danh sách theo dõi Valorant!"
                )
            else:
                await message.channel.send(
                    "❌ Cú pháp: `!track valorant <tên_riot> <tag_riot>`\n"
                    "Ví dụ: `!track valorant PlayerName 1234`"
                )
        except Exception as e:
            logger.error(f"Error adding tracked player: {str(e)}")
            await message.channel.send(f"❌ Lỗi: {str(e)}")
        return
    
    # Command: !untrack valorant
    if content.startswith("!untrack valorant"):
        try:
            discord_user_id = str(message.author.id)
            if discord_user_id in riot_tracker.tracked_players:
                player_info = riot_tracker.tracked_players[discord_user_id]
                riot_tracker.remove_tracked_player(discord_user_id)
                await message.channel.send(
                    f"✅ Đã xóa {player_info['riot_name']}#{player_info['riot_tag']} khỏi danh sách theo dõi!"
                )
            else:
                await message.channel.send("❌ Bạn chưa được thêm vào danh sách theo dõi.")
        except Exception as e:
            logger.error(f"Error removing tracked player: {str(e)}")
            await message.channel.send(f"❌ Lỗi: {str(e)}")
        return
    
    # Command: !set valorant channel
    if content.startswith("!set valorant channel"):
        try:
            if message.author.guild_permissions.administrator:
                riot_tracker.set_notification_channel(message.channel.id)
                await message.channel.send(
                    f"✅ Đã đặt kênh này ({message.channel.name}) làm kênh thông báo Valorant!"
                )
            else:
                await message.channel.send("❌ Bạn cần quyền Administrator để sử dụng lệnh này.")
        except Exception as e:
            logger.error(f"Error setting notification channel: {str(e)}")
            await message.channel.send(f"❌ Lỗi: {str(e)}")
        return
    
    # Command: !link riot <riot_name> <riot_tag>
    if content.startswith("!link riot"):
        try:
            parts = content.split()
            if len(parts) >= 4:
                riot_name = parts[2]
                riot_tag = parts[3]
                discord_user_id = str(message.author.id)
                
                # Link Discord to Riot account
                riot_tracker.link_discord_to_riot(discord_user_id, riot_name, riot_tag)
                # Also add to tracking
                riot_tracker.add_tracked_player(discord_user_id, riot_name, riot_tag)
                await message.channel.send(
                    f"✅ Đã liên kết tài khoản Discord của bạn với {riot_name}#{riot_tag}!\n"
                    f"Bot sẽ tự động theo dõi khi bạn chơi Valorant."
                )
            else:
                await message.channel.send(
                    "❌ Cú pháp: `!link riot <tên_riot> <tag_riot>`\n"
                    "Ví dụ: `!link riot PlayerName 1234`"
                )
        except Exception as e:
            logger.error(f"Error linking account: {str(e)}")
            await message.channel.send(f"❌ Lỗi: {str(e)}")
        return
    
    # Command: !list tracked
    if content.startswith("!list tracked"):
        try:
            if len(riot_tracker.tracked_players) == 0:
                await message.channel.send("📋 Chưa có người chơi nào được theo dõi.")
            else:
                players_list = []
                for discord_id, player_info in riot_tracker.tracked_players.items():
                    players_list.append(
                        f"• {player_info['riot_name']}#{player_info['riot_tag']}"
                    )
                await message.channel.send(
                    f"📋 **Danh sách người chơi được theo dõi:**\n" + "\n".join(players_list)
                )
        except Exception as e:
            logger.error(f"Error listing tracked players: {str(e)}")
            await message.channel.send(f"❌ Lỗi: {str(e)}")
        return
    
    # Process all other messages normally
    user_name = message.author.display_name
    prompt = message.content.strip()
    
    try:
        # Process message and send response (now async)
        logger.info(f"Processing message from {user_name}: {prompt}")
        response = await process_message(prompt, user_name)
        
        # Only send response if we got one
        if response:
            await message.channel.send(response)
    except Exception as e:
        logger.error(f"Lỗi khi xử lý tin nhắn: {str(e)}")

@bot.event
async def on_error(event, *args, **kwargs):
    logger.error(f"Lỗi trong event {event}: {str(args)} - {str(kwargs)}")

@bot.event
async def on_presence_update(before, after):
    """Detect when a user starts playing Valorant and auto-track them."""
    try:
        # Check if user started playing Valorant
        if not after.activity or not after.activity.name:
            return
        
        # Check if playing Valorant
        game_name = after.activity.name.lower()
        if "valorant" in game_name:
            discord_user_id = str(after.id)
            
            # Check if user has linked their Riot account
            if discord_user_id in riot_tracker.discord_to_riot:
                riot_info = riot_tracker.discord_to_riot[discord_user_id]
                riot_name = riot_info["riot_name"]
                riot_tag = riot_info["riot_tag"]
                
                # Auto-add to tracking if not already tracked
                if discord_user_id not in riot_tracker.tracked_players:
                    riot_tracker.add_tracked_player(discord_user_id, riot_name, riot_tag)
                    logger.info(f"Auto-tracked {after.display_name} ({riot_name}#{riot_tag}) - started playing Valorant")
            else:
                # User is playing Valorant but hasn't linked account
                # We could send a DM or message, but for now just log
                logger.info(f"User {after.display_name} is playing Valorant but hasn't linked Riot account")
                
    except Exception as e:
        logger.error(f"Error in presence update: {str(e)}")

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