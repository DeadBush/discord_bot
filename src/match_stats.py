import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

def parse_player_stats(match_data: Dict, puuid: str) -> Optional[Dict]:
    """Parse player stats from match data."""
    try:
        # Try different possible API response structures
        players = match_data.get("players", {})
        all_players = players.get("all_players", [])
        
        # If all_players is not in players, try direct access
        if not all_players:
            all_players = match_data.get("all_players", [])
        
        # Find the player in the match
        player_data = None
        for player in all_players:
            if player.get("puuid") == puuid:
                player_data = player
                break
        
        if not player_data:
            logger.warning(f"Player with PUUID {puuid} not found in match data")
            return None
        
        # Extract stats - handle different possible structures
        stats = player_data.get("stats", {})
        if not stats:
            stats = player_data  # Sometimes stats are at player level
        
        team = player_data.get("team", "")
        if not team:
            team = player_data.get("teamId", "")  # Alternative field name
        
        # Get team result
        teams = match_data.get("teams", {})
        team_result = None
        if team == "Red" or team == "red":
            team_result = teams.get("red", {}).get("has_won", False)
        elif team == "Blue" or team == "blue":
            team_result = teams.get("blue", {}).get("has_won", False)
        
        # Calculate score
        rounds_won = 0
        rounds_lost = 0
        if team == "Red" or team == "red":
            rounds_won = teams.get("red", {}).get("rounds_won", 0)
            rounds_lost = teams.get("blue", {}).get("rounds_won", 0)
        elif team == "Blue" or team == "blue":
            rounds_won = teams.get("blue", {}).get("rounds_won", 0)
            rounds_lost = teams.get("red", {}).get("rounds_won", 0)
        
        # Extract damage - handle different structures
        damage_made = 0
        damage_received = 0
        damage_data = stats.get("damage", {})
        if isinstance(damage_data, dict):
            damage_made = damage_data.get("made", damage_data.get("damage", 0))
            damage_received = damage_data.get("received", 0)
        elif isinstance(damage_data, (int, float)):
            damage_made = damage_data
        
        # Calculate totals for headshot percentage
        total_shots = stats.get("headshots", 0) + stats.get("bodyshots", 0) + stats.get("legshots", 0)
        
        return {
            "kills": stats.get("kills", 0),
            "deaths": stats.get("deaths", 0),
            "assists": stats.get("assists", 0),
            "score": stats.get("score", stats.get("combatScore", 0)),
            "headshots": stats.get("headshots", 0),
            "bodyshots": stats.get("bodyshots", 0),
            "legshots": stats.get("legshots", 0),
            "damage_made": damage_made,
            "damage_received": damage_received,
            "agent": player_data.get("character", player_data.get("agentId", "Unknown")),
            "team": team,
            "won": team_result if team_result is not None else False,
            "rounds_won": rounds_won,
            "rounds_lost": rounds_lost,
            "final_score": f"{rounds_won}-{rounds_lost}",
            "kd_ratio": round(stats.get("kills", 0) / max(stats.get("deaths", 1), 1), 2),
            "headshot_percentage": round((stats.get("headshots", 0) / max(total_shots, 1)) * 100, 1) if total_shots > 0 else 0.0
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
    
    message = f"""📊 **Thống kê trận đấu - {player_name}**
{win_emoji} **Kết quả:** {result_text} ({stats['final_score']})

🎯 **Tổng số:**
• K/D/A: {stats['kills']}/{stats['deaths']}/{stats['assists']} (K/D: {stats['kd_ratio']})
• Điểm số: {stats['score']}
• Sát thương: {stats['damage_made']}

🎪 **Agent:** {stats['agent']}
🎯 **Headshot:** {stats['headshot_percentage']}%
"""
    return message

