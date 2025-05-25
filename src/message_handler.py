import random
from src.constants import PERSONAL_INFO, FUNNY_RESPONSES, SPECIAL_USERS
from src.utils import is_vietnamese

def process_message(message, author):
    """Process incoming messages and return appropriate response."""
    # Convert message to lowercase for easier processing
    lower_message = message.lower()
    
    # Check if message is not in Vietnamese
    if not is_vietnamese(message):
        return "Tôi bị ngu"
        
    # Check for special users
    author_str = str(author)
    if author_str in SPECIAL_USERS:
        # Process personal info first
        personal_response = process_personal_info(lower_message)
        if personal_response:
            return SPECIAL_USERS[author_str] + personal_response
        # If no personal info response, return random or default
        return SPECIAL_USERS[author_str] + (random.choice(FUNNY_RESPONSES) if random.random() > 0.5 else "Tôi bị ngu")
        
    # Process personal information questions
    response = process_personal_info(lower_message)
    if response:
        return response
        
    # Return random response or default
    return random.choice(FUNNY_RESPONSES) if random.random() > 0.5 else "Tôi bị ngu"

def process_personal_info(message):
    """Process questions about personal information."""
    if 'tên' in message:
        return f"{PERSONAL_INFO['name']} đây! 😎"
    elif 'quê' in message or 'ở đâu' in message:
        return f"Tớ là dân {PERSONAL_INFO['hometown']} chính hiệu con rồng cháu tiên 😄"
    elif 'giới tính' in message:
        return f"{PERSONAL_INFO['gender']} nha, đẹp trai lắm 😌"
    elif 'học đại học' in message or 'đại học' in message:
        return f"Tớ là sinh viên {PERSONAL_INFO['university']} đó! 🎓"
    elif 'thcs' in message or 'cấp 2' in message:
        return f"Hồi cấp 2 tớ học ở {PERSONAL_INFO['middle_school']} 📚"
    elif 'thpt' in message or 'cấp 3' in message:
        return f"Tớ là cựu học sinh {PERSONAL_INFO['high_school']} nè 🏫"
    elif 'trường' in message:
        return f"Tớ tự hào khi là sinh viên {PERSONAL_INFO['university']} !!"
    return None 