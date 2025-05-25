import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.message_handler import process_message

class MockAuthor:
    """Mock Discord author object for testing"""
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name

def test_bot():
    """Interactive test function for bot responses"""
    print("=== Bot Testing Mode ===")
    print("Nhập 'exit' để thoát")
    print("Các tài khoản đặc biệt để test:")
    print("- DeadBush")
    print("- Kaisen#exson")
    print("- Skye._")
    print("\nChọn tên người dùng để test:")
    
    author_name = input("Tên người dùng (mặc định: TestUser): ").strip()
    if not author_name:
        author_name = "TestUser"
    
    mock_author = MockAuthor(author_name)
    
    while True:
        print("\n" + "="*50)
        message = input("\nNhập tin nhắn để test (hoặc 'exit' để thoát): ")
        
        if message.lower() == 'exit':
            break
            
        response = process_message(message, mock_author)
        print("\nBot trả lời:")
        print(f">>> {response}")

if __name__ == "__main__":
    test_bot() 