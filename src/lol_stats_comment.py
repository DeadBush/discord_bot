import os
import logging
from typing import Dict, Optional
from src.ai_handler import try_groq_api

logger = logging.getLogger(__name__)

async def generate_match_comment(stats: Dict, player_name: str) -> str:
    """Generate an AI comment in Vietnamese based on League of Legends match stats."""
    if not stats:
        return "Không có dữ liệu để phân tích."
    
    # Build stats summary for AI
    multi_kills = []
    if stats["penta_kills"] > 0:
        multi_kills.append(f"{stats['penta_kills']} Penta")
    if stats["quadra_kills"] > 0:
        multi_kills.append(f"{stats['quadra_kills']} Quadra")
    if stats["triple_kills"] > 0:
        multi_kills.append(f"{stats['triple_kills']} Triple")
    
    minutes = stats["game_duration"] // 60
    seconds = stats["game_duration"] % 60
    
    stats_summary = f"""
Thống kê trận đấu League of Legends của {player_name}:
- Kết quả: {'THẮNG' if stats['won'] else 'THUA'} (Thời gian: {minutes}:{seconds:02d})
- K/D/A: {stats['kills']}/{stats['deaths']}/{stats['assists']} (KDA ratio: {stats['kda_ratio']})
- Champion: {stats['champion']} ({stats['role']})
- CS: {stats['cs']} ({stats['cs_per_min']}/phút)
- Vàng kiếm được: {stats['gold_earned']:,}
- Sát thương gây ra: {stats['damage_dealt']:,}
- Sát thương nhận: {stats['damage_taken']:,}
- Vision Score: {stats['vision_score']}
- Multi-kills: {', '.join(multi_kills) if multi_kills else 'Không có'}
"""
    
    # Determine performance level
    kda = stats['kda_ratio']
    kills = stats['kills']
    won = stats['won']
    damage = stats['damage_dealt']
    
    performance = "xuất sắc" if kda >= 3.0 and kills >= 10 else \
                  "rất tốt" if kda >= 2.5 and kills >= 8 else \
                  "tốt" if kda >= 2.0 and kills >= 5 else \
                  "ổn" if kda >= 1.5 else \
                  "cần cải thiện"
    
    # Build prompt for AI
    system_prompt = """Bạn là một người bạn thân thiết, hài hước và châm biếm. Bạn đang xem thống kê trận đấu League of Legends của một người bạn và đưa ra nhận xét ngắn gọn, vui vẻ bằng tiếng Việt. Hãy:
- Đưa ra nhận xét dựa trên thống kê (KDA, damage, CS, multi-kills, v.v.)
- Nếu thắng và chơi tốt: khen ngợi nhưng đừng quá nghiêm túc, có thể châm biếm nhẹ
- Nếu thua hoặc chơi kém: động viên một cách hài hước, có thể châm biếm nhẹ nhàng
- Nếu có Penta/Quadra kill: đặc biệt khen ngợi
- Giữ tông điệu trẻ trung, vui vẻ, như một người bạn đang xem highlight
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
        if stats["penta_kills"] > 0:
            return f"🔥🔥🔥 PENTAKILL! Chơi như một vị thần! KDA {kda} là level pro rồi!"
        elif stats["quadra_kills"] > 0:
            return f"💥 QUADRA KILL! Chơi xuất sắc với KDA {kda}!"
        elif kda >= 3.0:
            return f"🔥 Chơi xuất sắc! KDA {kda} là level pro rồi đó!"
        elif kda >= 2.0:
            return f"💪 Chơi tốt lắm! Thắng với KDA {kda} là ổn rồi!"
        else:
            return f"🎉 Thắng rồi! Dù KDA chỉ {kda} nhưng quan trọng là team thắng!"
    else:
        if kda < 0.5:
            return f"😅 Hơi khó khăn nhỉ? KDA {kda}... Lần sau sẽ tốt hơn!"
        elif kda < 1.0:
            return f"💪 Gần rồi! KDA {kda} cần cải thiện thêm chút nữa thôi!"
        else:
            return f"🤝 Thua nhưng chơi ổn! KDA {kda} không tệ đâu!"

