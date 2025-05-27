import random
from src.constants import PERSONAL_INFO, FUNNY_RESPONSES, SPECIAL_RESPONSES, SPECIAL_USERS
from src.utils import is_user_DeadBush, is_user_ToMan, is_user_Skye, is_user_Kaisen

def process_message(message, user_name):
    """Process incoming messages and return appropriate response."""
    # Convert message to lowercase for easier processing
    lower_message = message.lower()


    # Author string
    author_str = str(user_name)
    print(f"Author string: {author_str}")


    # Check if user is DeadBush
    if is_user_DeadBush(author_str):
    # Check if message is not in Vietnamese
        if author_str in SPECIAL_USERS:
            # Process personal info first

            personal_response = process_personal_info(lower_message)
            special_response = process_special_responses(lower_message)

            if personal_response:
                return SPECIAL_USERS[author_str] + personal_response
            
            if special_response:
                return SPECIAL_USERS[author_str] + special_response
            # If no personal info response, return random or default
            return SPECIAL_USERS[author_str] + (random.choice(FUNNY_RESPONSES) if random.random() > 0.5 else "Tôi bị ngu")
    


    #Check if user is Skye._
    if is_user_Skye(user_name):
    # Check if message is not in Vietnamese   
        if author_str in SPECIAL_USERS:
            # Process personal info first

            personal_response = process_personal_info(lower_message)
            special_response = process_special_responses(lower_message)

            if personal_response:
                return SPECIAL_USERS[author_str] + personal_response
            
            if special_response:
                return SPECIAL_USERS[author_str] + special_response
            # If no personal info response, return random or default
            return SPECIAL_USERS[author_str] + (random.choice(FUNNY_RESPONSES) if random.random() > 0.5 else "Tôi bị ngu")
        
    #Check if user is Kaisen#exson
    if is_user_Kaisen(user_name):
    # Check if message is not in Vietnamese    
        if author_str in SPECIAL_USERS:
            # Process personal info first

            personal_response = process_personal_info(lower_message)
            special_response = process_special_responses(lower_message)

            if personal_response:
                return SPECIAL_USERS[author_str] + personal_response
            
            if special_response:
                return SPECIAL_USERS[author_str] + special_response
            
            # If no personal info response, return random or default
            return SPECIAL_USERS[author_str] + (random.choice(FUNNY_RESPONSES) if random.random() > 0.5 else "Tôi bị ngu")
    

    
    #Check if user is To Man
    if is_user_ToMan(user_name):
    # Check if message is not in Vietnamese     
        # Check for special users
        if author_str in SPECIAL_USERS:
            # Process personal info first

            personal_response = process_personal_info(lower_message)
            special_response = process_special_responses(lower_message)

            if personal_response:
                return SPECIAL_USERS[author_str] + personal_response
            
            if special_response:
                return SPECIAL_USERS[author_str] + special_response
            
            # If no personal info response, return random or default
            return SPECIAL_USERS[author_str] + (random.choice(FUNNY_RESPONSES) if random.random() > 0.5 else "Tôi bị ngu")
        



    # Process personal information questions
    response = process_personal_info(lower_message) or process_special_responses(lower_message)
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
    elif 'ngày sinh' in message or 'sinh nhật' in message or 'sinh ngày' in message or 'tuổi' in message:
        return f"Tớ sinh ngày {PERSONAL_INFO['birthday']} nè! 🎂"
    return None 

def process_special_responses(message):
    """Process special responses."""
    if "Minh" in message or "minh" in message:
        return f"{SPECIAL_RESPONSES['Minh']}"
    elif "Mẫn" in message or "mẫn" in message:
        return f"{SPECIAL_RESPONSES['Mẫn']}"
    return None