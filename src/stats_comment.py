import os
import logging
from typing import Dict, Optional
from src.ai_handler import try_groq_api

logger = logging.getLogger(__name__)

async def generate_match_comment(stats: Dict, player_name: str) -> str:
    """Generate an AI comment in Vietnamese based on match stats."""
    if not stats:
        return "Không có dữ liệu để phân tích."
    
    # Build stats summary for AI
    stats_summary = f"""
Thống kê trận đấu Valorant của {player_name}:
- Kết quả: {'THẮNG' if stats['won'] else 'THUA'} với tỷ số {stats['final_score']}
- K/D/A: {stats['kills']}/{stats['deaths']}/{stats['assists']} (K/D ratio: {stats['kd_ratio']})
- Điểm số: {stats['score']}
- Sát thương gây ra: {stats['damage_made']}
- Sát thương nhận: {stats['damage_received']}
- Headshot: {stats['headshot_percentage']}%
- Agent sử dụng: {stats['agent']}
"""
    
    # Determine performance level
    kd = stats['kd_ratio']
    kills = stats['kills']
    won = stats['won']
    
    performance = "xuất sắc" if kd >= 2.0 and kills >= 20 else \
                  "tốt" if kd >= 1.5 and kills >= 15 else \
                  "ổn" if kd >= 1.0 else \
                  "cần cải thiện"
    
    # Build prompt for AI
    system_prompt = """Bạn là một người bạn thân thiết, hài hước và châm biếm. Bạn đang xem thống kê trận đấu Valorant của một người bạn và đưa ra nhận xét ngắn gọn, vui vẻ bằng tiếng Việt. Hãy:
- Đưa ra nhận xét dựa trên thống kê
- Nếu thắng và chơi tốt: khen ngợi nhưng đừng quá nghiêm túc
- Nếu thua hoặc chơi kém: động viên một cách hài hước, có thể châm biếm nhẹ nhàng
- Giữ tông điệu trẻ trung, vui vẻ
- Chỉ viết 1-2 câu ngắn gọn
- Không quá dài dòng"""
    
    user_message = f"{stats_summary}\nHãy đưa ra một nhận xét ngắn gọn và hài hước về trận đấu này:"
    
    try:
        comment = await try_groq_api(system_prompt, user_message, "")
        if comment:
            return comment.strip()
    except Exception as e:
        logger.error(f"Error generating AI comment: {str(e)}")
    
    # Fallback to simple comment
    if won:
        if kd >= 2.0:
            return f"🔥 Chơi xuất sắc! {kd} K/D là level pro rồi đó!"
        elif kd >= 1.5:
            return f"💪 Chơi tốt lắm! Thắng với {kd} K/D là ổn rồi!"
        else:
            return f"🎉 Thắng rồi! Dù K/D chỉ {kd} nhưng quan trọng là team thắng!"
    else:
        if kd < 0.5:
            return f"😅 Hơi khó khăn nhỉ? K/D {kd}... Lần sau sẽ tốt hơn!"
        elif kd < 1.0:
            return f"💪 Gần rồi! K/D {kd} cần cải thiện thêm chút nữa thôi!"
        else:
            return f"🤝 Thua nhưng chơi ổn! K/D {kd} không tệ đâu!"

