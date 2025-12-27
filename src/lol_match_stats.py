import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

def parse_player_stats(match_data: Dict, puuid: str) -> Optional[Dict]:
    """Parse player stats from League of Legends match data."""
    try:
        # League API structure: info.participants
        info = match_data.get("info", {})
        participants = info.get("participants", [])
        
        # Find the player in the match
        player_data = None
        for participant in participants:
            if participant.get("puuid") == puuid:
                player_data = participant
                break
        
        if not player_data:
            logger.warning(f"Player with PUUID {puuid} not found in match data")
            return None
        
        # Extract stats
        stats = player_data.get("stats", {})
        team_id = player_data.get("teamId", 0)  # 100 for blue, 200 for red
        
        # Get team result
        teams = info.get("teams", [])
        team_result = None
        for team in teams:
            if team.get("teamId") == team_id:
                team_result = team.get("win", False)
                break
        
        # Get game mode and duration
        game_mode = info.get("gameMode", "Unknown")
        game_duration = info.get("gameDuration", 0)  # in seconds
        
        # Calculate KDA
        kills = stats.get("kills", 0)
        deaths = stats.get("deaths", 0)
        assists = stats.get("assists", 0)
        
        # Calculate damage stats
        total_damage_dealt = stats.get("totalDamageDealtToChampions", 0)
        total_damage_taken = stats.get("totalDamageTaken", 0)
        
        # Vision score
        vision_score = stats.get("visionScore", 0)
        
        # CS (Creep Score)
        total_minions_killed = stats.get("totalMinionsKilled", 0)
        neutral_minions_killed = stats.get("neutralMinionsKilled", 0)
        total_cs = total_minions_killed + neutral_minions_killed
        
        # Gold
        gold_earned = stats.get("goldEarned", 0)
        
        # Champion
        champion_id = player_data.get("championId", 0)
        champion_name = player_data.get("championName", "Unknown")
        
        # Role and lane
        team_position = player_data.get("teamPosition", "")
        individual_position = player_data.get("individualPosition", "")
        role = individual_position if individual_position else team_position
        
        # Items
        items = [
            stats.get("item0", 0),
            stats.get("item1", 0),
            stats.get("item2", 0),
            stats.get("item3", 0),
            stats.get("item4", 0),
            stats.get("item5", 0),
            stats.get("item6", 0),  # Trinket
        ]
        
        # Multi-kills
        double_kills = stats.get("doubleKills", 0)
        triple_kills = stats.get("tripleKills", 0)
        quadra_kills = stats.get("quadraKills", 0)
        penta_kills = stats.get("pentaKills", 0)
        
        # Calculate KDA ratio
        kda_ratio = round((kills + assists) / max(deaths, 1), 2)
        
        # Calculate CS per minute
        minutes = game_duration / 60 if game_duration > 0 else 1
        cs_per_min = round(total_cs / minutes, 1)
        
        return {
            "kills": kills,
            "deaths": deaths,
            "assists": assists,
            "kda_ratio": kda_ratio,
            "champion": champion_name,
            "champion_id": champion_id,
            "role": role,
            "won": team_result if team_result is not None else False,
            "damage_dealt": total_damage_dealt,
            "damage_taken": total_damage_taken,
            "vision_score": vision_score,
            "cs": total_cs,
            "cs_per_min": cs_per_min,
            "gold_earned": gold_earned,
            "game_duration": game_duration,
            "game_mode": game_mode,
            "double_kills": double_kills,
            "triple_kills": triple_kills,
            "quadra_kills": quadra_kills,
            "penta_kills": penta_kills,
            "items": items
        }
    except Exception as e:
        logger.error(f"Error parsing player stats: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return None

def format_match_stats(stats: Dict, player_name: str) -> str:
    """Format match stats into a readable string."""
    if not stats:
        return f"📊 Không thể lấy thống kê cho {player_name}"
    
    win_emoji = "✅" if stats["won"] else "❌"
    result_text = "THẮNG" if stats["won"] else "THUA"
    
    # Format game duration
    minutes = stats["game_duration"] // 60
    seconds = stats["game_duration"] % 60
    duration_str = f"{minutes}:{seconds:02d}"
    
    # Multi-kill summary
    multi_kills = []
    if stats["penta_kills"] > 0:
        multi_kills.append(f"{stats['penta_kills']} Penta")
    if stats["quadra_kills"] > 0:
        multi_kills.append(f"{stats['quadra_kills']} Quadra")
    if stats["triple_kills"] > 0:
        multi_kills.append(f"{stats['triple_kills']} Triple")
    if stats["double_kills"] > 0:
        multi_kills.append(f"{stats['double_kills']} Double")
    multi_kill_str = ", ".join(multi_kills) if multi_kills else "Không có"
    
    message = f"""📊 **Thống kê trận đấu League of Legends - {player_name}**
{win_emoji} **Kết quả:** {result_text} ({duration_str})

🎯 **K/D/A:** {stats['kills']}/{stats['deaths']}/{stats['assists']} (KDA: {stats['kda_ratio']})
⚔️ **Champion:** {stats['champion']} ({stats['role']})

💰 **Kinh tế:**
• CS: {stats['cs']} ({stats['cs_per_min']}/phút)
• Vàng kiếm được: {stats['gold_earned']:,}

💥 **Sát thương:**
• Gây ra: {stats['damage_dealt']:,}
• Nhận: {stats['damage_taken']:,}

👁️ **Vision Score:** {stats['vision_score']}
🔥 **Multi-kills:** {multi_kill_str}
"""
    return message

