import os
import logging
import asyncio
import base64
import json
import requests
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class RiotTracker:
    """Tracks Valorant matches using Riot Games API."""
    
    def __init__(self):
        self.api_key = os.getenv("RIOT_API_KEY")
        self.region = os.getenv("RIOT_REGION", "ap")  # ap, na, eu, kr, etc.
        self.tracked_players: Dict[str, Dict] = {}  # {discord_user_id: {riot_name, riot_tag, puuid, last_match_id, in_match}}
        self.last_match_ids: Dict[str, str] = {}  # {riot_puuid: last_match_id}
        self.notification_channel_id = None
        self.is_running = False
        self.check_interval = 30  # Check every 30 seconds
        self.discord_to_riot: Dict[str, Dict] = {}  # {discord_user_id: {riot_name, riot_tag}} - for auto-tracking
        
    def set_notification_channel(self, channel_id: int):
        """Set the Discord channel ID for notifications."""
        self.notification_channel_id = channel_id
        
    def link_discord_to_riot(self, discord_user_id: str, riot_name: str, riot_tag: str):
        """Link a Discord user to their Riot account for auto-tracking."""
        self.discord_to_riot[discord_user_id] = {
            "riot_name": riot_name,
            "riot_tag": riot_tag
        }
        logger.info(f"Linked Discord user {discord_user_id} to {riot_name}#{riot_tag}")
        
    def add_tracked_player(self, discord_user_id: str, riot_name: str, riot_tag: str):
        """Add a player to track."""
        self.tracked_players[discord_user_id] = {
            "riot_name": riot_name,
            "riot_tag": riot_tag,
            "puuid": None,
            "last_match_id": None,
            "in_match": False,
            "current_match_id": None
        }
        logger.info(f"Added tracked player: {riot_name}#{riot_tag} (Discord: {discord_user_id})")
        
    def remove_tracked_player(self, discord_user_id: str):
        """Remove a player from tracking."""
        if discord_user_id in self.tracked_players:
            del self.tracked_players[discord_user_id]
            logger.info(f"Removed tracked player: {discord_user_id}")
            
    async def get_player_puuid(self, riot_name: str, riot_tag: str) -> Optional[str]:
        """Get player PUUID from Riot API."""
        if not self.api_key:
            logger.warning("RIOT_API_KEY not set, cannot get player PUUID")
            return None
            
        try:
            # Account API uses americas, asia, europe regions
            # For Asia Pacific, use 'asia' region
            account_region = "asia" if self.region.lower() == "ap" else "americas"
            url = f"https://{account_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{riot_name}/{riot_tag}"
            headers = {"X-Riot-Token": self.api_key}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("puuid")
            elif response.status_code == 404:
                logger.warning(f"Player {riot_name}#{riot_tag} not found")
            elif response.status_code == 403:
                logger.warning("Riot API key may not have access. Check your API key permissions.")
            else:
                logger.error(f"Error getting PUUID: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Exception getting player PUUID: {str(e)}")
            
        return None
        
    def _get_valorant_region(self) -> str:
        """Convert Riot region to Valorant region shard."""
        # Valorant uses different region shards
        region_map = {
            "ap": "ap",  # Asia Pacific
            "na": "na",  # North America
            "eu": "eu",  # Europe
            "kr": "kr",  # Korea
            "br": "br",  # Brazil
            "latam": "latam",  # Latin America
        }
        return region_map.get(self.region.lower(), "ap")
        
    async def get_current_match(self, puuid: str) -> Optional[Dict]:
        """Get current active match for a player."""
        if not self.api_key:
            return None
            
        try:
            # Valorant uses region shards (ap, na, eu, kr, br, latam)
            valorant_region = self._get_valorant_region()
            url = f"https://{valorant_region}.api.riotgames.com/val/active/v1/active-match/by-puuid/{puuid}"
            headers = {"X-Riot-Token": self.api_key}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                # Player is not in a match
                return None
            elif response.status_code == 403:
                logger.warning("Riot API key may not have Valorant API access. You may need to apply for production access.")
            else:
                logger.error(f"Error getting current match: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Exception getting current match: {str(e)}")
            
        return None
        
    async def get_recent_matches(self, puuid: str, count: int = 1) -> List[Dict]:
        """Get recent match history for a player."""
        if not self.api_key:
            return []
            
        try:
            # Valorant uses region shards
            valorant_region = self._get_valorant_region()
            url = f"https://{valorant_region}.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}"
            headers = {"X-Riot-Token": self.api_key}
            params = {"start": 0, "count": count}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("history", [])
            elif response.status_code == 403:
                logger.warning("Riot API key may not have Valorant API access. You may need to apply for production access.")
            else:
                logger.error(f"Error getting match history: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Exception getting match history: {str(e)}")
            
        return []
        
    async def get_match_details(self, match_id: str) -> Optional[Dict]:
        """Get detailed match information including stats."""
        if not self.api_key:
            return None
            
        try:
            valorant_region = self._get_valorant_region()
            url = f"https://{valorant_region}.api.riotgames.com/val/match/v1/matches/{match_id}"
            headers = {"X-Riot-Token": self.api_key}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                logger.warning("Riot API key may not have Valorant API access.")
            else:
                logger.error(f"Error getting match details: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Exception getting match details: {str(e)}")
            
        return None
        
    async def check_for_new_matches(self) -> List[Dict]:
        """Check all tracked players for new matches."""
        new_matches = []
        
        for discord_user_id, player_info in self.tracked_players.items():
            try:
                riot_name = player_info["riot_name"]
                riot_tag = player_info["riot_tag"]
                
                # Get PUUID if not cached
                if not player_info["puuid"]:
                    puuid = await self.get_player_puuid(riot_name, riot_tag)
                    if puuid:
                        player_info["puuid"] = puuid
                    else:
                        continue
                else:
                    puuid = player_info["puuid"]
                
                # First, try to get current active match
                current_match = await self.get_current_match(puuid)
                
                if current_match:
                    match_id = current_match.get("MatchID")
                    was_in_match = player_info.get("in_match", False)
                    
                    # If player just entered a match
                    if not was_in_match:
                        player_info["in_match"] = True
                        player_info["current_match_id"] = match_id
                        player_info["last_match_id"] = match_id
                        new_matches.append({
                            "discord_user_id": discord_user_id,
                            "riot_name": riot_name,
                            "riot_tag": riot_tag,
                            "match_id": match_id,
                            "match_data": current_match,
                            "is_active": True
                        })
                        logger.info(f"New active match detected for {riot_name}#{riot_tag}: {match_id}")
                else:
                    # Player is not in a match anymore
                    was_in_match = player_info.get("in_match", False)
                    if was_in_match:
                        # Match just ended, get match details
                        player_info["in_match"] = False
                        ended_match_id = player_info.get("current_match_id")
                        if ended_match_id:
                            # Get match details for stats
                            match_details = await self.get_match_details(ended_match_id)
                            if match_details:
                                new_matches.append({
                                    "discord_user_id": discord_user_id,
                                    "riot_name": riot_name,
                                    "riot_tag": riot_tag,
                                    "match_id": ended_match_id,
                                    "match_data": match_details,
                                    "is_active": False,
                                    "match_ended": True
                                })
                                logger.info(f"Match ended for {riot_name}#{riot_tag}: {ended_match_id}")
                        player_info["current_match_id"] = None
                    else:
                        # If no active match and wasn't in match, check recent match history for new matches
                        recent_matches = await self.get_recent_matches(puuid, count=1)
                        
                        if recent_matches and len(recent_matches) > 0:
                            latest_match = recent_matches[0]
                            match_id = latest_match.get("matchId")
                            last_match_id = player_info.get("last_match_id")
                            
                            # Check if this is a new match (not the same as last known)
                            if match_id and match_id != last_match_id:
                                # Only notify if the match is very recent (within last 5 minutes)
                                # This helps avoid notifying about old matches
                                match_time = latest_match.get("gameStartTimeMillis", 0)
                                if match_time:
                                    from datetime import datetime
                                    match_datetime = datetime.fromtimestamp(match_time / 1000)
                                    time_diff = (datetime.now() - match_datetime).total_seconds()
                                    
                                    # Only notify if match started within last 5 minutes
                                    if time_diff < 300:  # 5 minutes
                                        player_info["last_match_id"] = match_id
                                        new_matches.append({
                                            "discord_user_id": discord_user_id,
                                            "riot_name": riot_name,
                                            "riot_tag": riot_tag,
                                            "match_id": match_id,
                                            "match_data": latest_match,
                                            "is_active": False
                                        })
                                        logger.info(f"New match detected for {riot_name}#{riot_tag}: {match_id}")
                
            except Exception as e:
                logger.error(f"Error checking matches for player {discord_user_id}: {str(e)}")
                
        return new_matches
        
    async def start_monitoring(self, bot, check_interval: int = 30):
        """Start the background monitoring task."""
        if self.is_running:
            logger.warning("Monitoring is already running")
            return
            
        self.is_running = True
        self.check_interval = check_interval
        logger.info(f"Starting Valorant match monitoring (interval: {check_interval}s)")
        
        # Initialize PUUIDs for all tracked players
        for discord_user_id, player_info in self.tracked_players.items():
            if not player_info.get("puuid"):
                puuid = await self.get_player_puuid(
                    player_info["riot_name"],
                    player_info["riot_tag"]
                )
                if puuid:
                    player_info["puuid"] = puuid
                    
        # Start monitoring loop
        while self.is_running:
            try:
                new_matches = await self.check_for_new_matches()
                
                # Send notifications for new matches
                if new_matches and self.notification_channel_id:
                    channel = bot.get_channel(self.notification_channel_id)
                    if channel:
                        for match in new_matches:
                            if match.get("match_ended", False):
                                # Match ended - send stats
                                await self.send_match_end_notification(channel, match, bot)
                            elif match.get("is_active", False):
                                message = (
                                    f"🎮 **{match['riot_name']}#{match['riot_tag']}** "
                                    f"đang trong trận đấu Valorant!"
                                )
                                await channel.send(message)
                                logger.info(f"Sent notification for {match['riot_name']}#{match['riot_tag']}")
                            else:
                                message = (
                                    f"🎮 **{match['riot_name']}#{match['riot_tag']}** "
                                    f"đã bắt đầu một trận đấu Valorant!"
                                )
                                await channel.send(message)
                                logger.info(f"Sent notification for {match['riot_name']}#{match['riot_tag']}")
                
                await asyncio.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                await asyncio.sleep(self.check_interval)
                
    async def send_match_end_notification(self, channel, match: Dict, bot):
        """Send match end notification with stats and AI comment."""
        try:
            from src.match_stats import parse_player_stats, format_match_stats
            from src.stats_comment import generate_match_comment
            
            player_info = self.tracked_players.get(match["discord_user_id"])
            if not player_info or not player_info.get("puuid"):
                return
            
            puuid = player_info["puuid"]
            match_data = match.get("match_data", {})
            
            # Parse stats
            stats = parse_player_stats(match_data, puuid)
            if not stats:
                await channel.send(
                    f"🎮 **{match['riot_name']}#{match['riot_tag']}** đã kết thúc trận đấu!"
                )
                return
            
            # Format stats message
            stats_message = format_match_stats(stats, f"{match['riot_name']}#{match['riot_tag']}")
            
            # Generate AI comment
            ai_comment = await generate_match_comment(stats, f"{match['riot_name']}#{match['riot_tag']}")
            
            # Send combined message
            full_message = f"{stats_message}\n💬 **Nhận xét:** {ai_comment}"
            await channel.send(full_message)
            logger.info(f"Sent match end stats for {match['riot_name']}#{match['riot_tag']}")
            
        except Exception as e:
            logger.error(f"Error sending match end notification: {str(e)}")
            # Fallback to simple message
            try:
                await channel.send(
                    f"🎮 **{match['riot_name']}#{match['riot_tag']}** đã kết thúc trận đấu!"
                )
            except:
                pass
    
    def stop_monitoring(self):
        """Stop the background monitoring task."""
        self.is_running = False
        logger.info("Stopped Valorant match monitoring")

# Global tracker instance
riot_tracker = RiotTracker()

