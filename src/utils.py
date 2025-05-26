from src.constants import SPECIAL_USERS


def is_vietnamese(text):
    """Check if the text contains Vietnamese characters."""
    # Define Vietnamese diacritical marks and special characters
    vietnamese_chars = "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ"
    # Check if text contains Latin characters
    has_latin = any(c.isascii() and c.isalpha() for c in text)
    # Check if text contains Vietnamese characters
    has_vietnamese = any(c in vietnamese_chars for c in text.lower())
    return not (has_latin and not has_vietnamese) 

### Check user hiearchy ###
# User is DeadBush
def is_user_DeadBush(author_str):
    # Check if user is DeadBush
    if author_str == "DeadBush":
        return True
    return False

# User is Skye._
def is_user_Skye(author_str):
    # Check if user is Skye._
    if author_str == "Skye._":
        return True
    return False   

# User is Kaisen#exson
def is_user_Kaisen(author_str):
    # Check if user is Kaisen#exson
    if author_str == "Kaisen#exson":
        return True
    return False

# User is Toman
def is_user_ToMan(author_str):
    # Check if user is To Man
    if author_str == "To Man":
        return True
    return False