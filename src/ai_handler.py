import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def load_prompts():
    """Load prompts from prompts.txt file."""
    try:
        with open('prompts.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        logger.warning("prompts.txt not found, using default prompts")
        return """Họ tên: Nguyễn Đình Thống
Quê quán: Bắc Ninh, Hà Nội, Việt Nam
Giới tính: Nam
Trường đại học: Đại Học Khoa Học Tự Nhiên - ĐHQG Hà Nội
Trường Trung học Cơ sở: THCS Nguyễn Văn Trỗi
Trường Trung học Phổ thông: Trường THPT Phú Nhuận
Cách xử lý tin nhắn kiểu: đùa cợt, trẻ trung, châm biếm.
Chỉ nói tiếng Việt, nếu nói ngôn ngữ khác thì trả lời là "Tôi bị ngu"
Những câu hỏi không nằm trong pattern trả lời là "Tôi bị ngu"
"""

def build_system_prompt():
    """Build system prompt from prompts.txt."""
    prompts = load_prompts()
    system_prompt = f"""Bạn là một chatbot Discord tên là Nguyễn Đình Thống. Hãy trả lời các câu hỏi dựa trên thông tin sau:

{prompts}

Hãy trả lời một cách tự nhiên, đùa cợt, trẻ trung và châm biếm như đã yêu cầu. Chỉ trả lời bằng tiếng Việt."""
    return system_prompt

async def get_ai_response(user_message: str, user_name: str = "") -> str:
    """
    Get AI response using free AI model.
    Tries Groq first, falls back to Hugging Face if needed.
    """
    system_prompt = build_system_prompt()
    
    # Try Groq API first (free and fast)
    groq_response = await try_groq_api(system_prompt, user_message, user_name)
    if groq_response:
        return groq_response
    
    # Fallback to Hugging Face
    hf_response = await try_huggingface_api(system_prompt, user_message, user_name)
    if hf_response:
        return hf_response
    
    # Final fallback
    return "Tôi bị ngu"

async def try_groq_api(system_prompt: str, user_message: str, user_name: str) -> str:
    """Try to get response from Groq API."""
    try:
        from groq import Groq
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.warning("GROQ_API_KEY not found in environment variables")
            return None
        
        client = Groq(api_key=api_key)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Free and fast model
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    except ImportError:
        logger.warning("groq package not installed")
        return None
    except Exception as e:
        logger.error(f"Error calling Groq API: {str(e)}")
        return None

async def try_huggingface_api(system_prompt: str, user_message: str, user_name: str) -> str:
    """Try to get response from Hugging Face Inference API."""
    try:
        import requests
        
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        model = "vinai/PhoGPT-7B5-Instruct"  # Vietnamese model
        
        # If no API key, try without authentication (may have rate limits)
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        # Build prompt
        full_prompt = f"{system_prompt}\n\nNgười dùng: {user_message}\nBạn:"
        
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{model}",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "").strip()
            elif isinstance(result, dict):
                return result.get("generated_text", "").strip()
        
        logger.warning(f"Hugging Face API returned status {response.status_code}")
        return None
    except ImportError:
        logger.warning("requests package not installed")
        return None
    except Exception as e:
        logger.error(f"Error calling Hugging Face API: {str(e)}")
        return None

