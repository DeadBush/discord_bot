def is_vietnamese(text):
    """Check if the text contains Vietnamese characters."""
    # Define Vietnamese diacritical marks and special characters
    vietnamese_chars = "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ"
    # Check if text contains Latin characters
    has_latin = any(c.isascii() and c.isalpha() for c in text)
    # Check if text contains Vietnamese characters
    has_vietnamese = any(c in vietnamese_chars for c in text.lower())
    return not (has_latin and not has_vietnamese) 