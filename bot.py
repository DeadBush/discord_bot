import discord
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Personal information
personal_info = {
    "name": "Nguyễn Đình Thống",
    "hometown": "Bắc Ninh, Hà Nội, Việt Nam",
    "gender": "Nam",
    "university": "Đại Học Khoa Học Tự Nhiên - ĐHQG Hà Nội",
    "middle_school": "THCS Nguyễn Văn Trỗi",
    "high_school": "Trường THPT Phú Nhuận"
}

# Funny responses for random selection
funny_responses = [
    "Hehe, câu này hay đấy! 😆",
    "Thú vị ghê! 🤔",
    "Để tớ suy nghĩ tí... À mà thôi, tớ lười suy nghĩ rồi 😪",
    "Bạn thật là thông minh... khác hẳn tớ 😅",
    "Tớ đang bận chơi game, hỏi câu khác đi 🎮"
]

def is_vietnamese(text):
    # Define Vietnamese diacritical marks and special characters
    vietnamese_chars = "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ"
    # Check if text contains Latin characters
    has_latin = any(c.isascii() and c.isalpha() for c in text)
    # Check if text contains Vietnamese characters
    has_vietnamese = any(c in vietnamese_chars for c in text.lower())
    return not (has_latin and not has_vietnamese)

def process_message(message):
    # Chuyển message về chữ thường để dễ xử lý
    lower_message = message.lower()
    
    # Kiểm tra nếu có người giả mạo
    if "@yomsi." in message:
        return "Thằng này giả mạo tôi!"
    
    # Kiểm tra nếu là bạn thân
    if "@minhden." in message:
        return "Đây là bạn thân của tôi!"
    
    # Kiểm tra nếu tin nhắn không phải tiếng Việt
    if not is_vietnamese(message):
        return "Tôi bị ngu"

    # Xử lý các câu hỏi về thông tin cá nhân
    if 'tên' in lower_message:
        return f"{personal_info['name']} đây! 😎"
    if 'quê' in lower_message or 'ở đâu' in lower_message:
        return f"Tớ là dân {personal_info['hometown']} chính hiệu con rồng cháu tiên 😄"
    if 'giới tính' in lower_message:
        return f"{personal_info['gender']} nha, đẹp trai lắm 😌"
    if 'học đại học' in lower_message or 'đại học' in lower_message:
        return f"Tớ là sinh viên {personal_info['university']} đó! 🎓"
    if 'thcs' in lower_message or 'cấp 2' in lower_message:
        return f"Hồi cấp 2 tớ học ở {personal_info['middle_school']} 📚"
    if 'thpt' in lower_message or 'cấp 3' in lower_message:
        return f"Tớ là cựu học sinh {personal_info['high_school']} nè 🏫"

    # Nếu không match với các pattern trên, trả về câu trả lời ngẫu nhiên hoặc "Tôi bị ngu"
    return random.choice(funny_responses) if random.random() > 0.5 else "Tôi bị ngu"

@bot.event
async def on_ready():
    print(f'{bot.user} đã sẵn sàng phục vụ!')

@bot.event
async def on_message(message):
    # Bỏ qua tin nhắn từ bot
    if message.author == bot.user:
        return

    # Xử lý tin nhắn
    response = process_message(message.content)
    await message.channel.send(response)

# Run the bot
try:
    bot.run(TOKEN)
except Exception as e:
    print(f"Lỗi khi khởi động bot: {str(e)}")