import os
import logging
import asyncio
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class LeagueTracker:
    """Tracks League of Legends matches using Riot Games API."""
    
    def __init__(self):
        self.api_key = os.getenv("RIOT_API_KEY")
        self.region = os.getenv("RIOT_REGION", "ap")  # ap, na, eu, kr, etc.
        self.tracked_players: Dict[str, Dict] = {}  # {discord_user_id: {riot_name, riot_tag, puuid, summoner_id, last_match_id, in_match}}
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
        logger.info(f"Linked Discord user {discord_user_id} to {riot_name}#{riot_tag} (LoL)")
        
    def add_tracked_player(self, discord_user_id: str, riot_name: str, riot_tag: str):
        """Add a player to track."""
        self.tracked_players[discord_user_id] = {
            "riot_name": riot_name,
            "riot_tag": riot_tag,
            "puuid": None,
            "summoner_id": None,
            "last_match_id": None,
            "in_match": False,
            "current_match_id": None
        }
        logger.info(f"Added tracked player: {riot_name}#{riot_tag} (Discord: {discord_user_id}) - LoL")
        
    def remove_tracked_player(self, discord_user_id: str):
        """Remove a player from tracking."""
        if discord_user_id in self.tracked_players:
            del self.tracked_players[discord_user_id]
            logger.info(f"Removed tracked player: {discord_user_id} - LoL")
            
    def _get_lol_region(self) -> str:
        """Convert Riot region to League of Legends region."""
        # League uses specific region codes - "ap" is NOT a valid LoL region
        # Common regions: kr, jp1, oc1, vn2, ph2, sg2, th2, tw2
        region_map = {
            "na": "na1",  # North America
            "na1": "na1",
            "eu": "euw1",  # Europe West (default for EU)
            "euw": "euw1",
            "euw1": "euw1",
            "eune": "eun1",  # Europe Nordic & East
            "eun": "eun1",
            "eun1": "eun1",
            "kr": "kr",  # Korea
            "br": "br1",  # Brazil
            "br1": "br1",
            "latam": "la1",  # Latin America North
            "la1": "la1",
            "la2": "la2",  # Latin America South
            "oce": "oc1",  # Oceania
            "oc1": "oc1",
            "ru": "ru",  # Russia
            "tr": "tr1",  # Turkey
            "tr1": "tr1",
            "jp": "jp1",  # Japan
            "jp1": "jp1",
            "ph": "ph2",  # Philippines
            "ph2": "ph2",
            "sg": "sg2",  # Singapore
            "sg2": "sg2",
            "th": "th2",  # Thailand
            "th2": "th2",
            "tw": "tw2",  # Taiwan
            "tw2": "tw2",
            "vn": "vn2",  # Vietnam
            "vn2": "vn2",
        }
        
        region_lower = self.region.lower()
        
        # If "ap" is specified, we need to try common Asia Pacific regions
        # Default to KR as it's the most common
        if region_lower == "ap":
            logger.warning(
                "⚠️ Region 'ap' is not valid for League of Legends API.\n"
                "Please set RIOT_REGION to a specific region like: kr, jp1, oc1, vn2, ph2, sg2, th2, tw2\n"
                "Defaulting to 'kr' for now, but this may cause 403 errors if the player is not in KR region."
            )
            return "kr"
        
        mapped_region = region_map.get(region_lower, "na1")
        
        if mapped_region == "na1" and region_lower not in ["na", "na1"]:
            logger.warning(f"Unknown region '{self.region}', defaulting to 'na1'. This may cause issues.")
        
        return mapped_region
        
    def _get_account_region(self) -> str:
        """Get account API region."""
        # Account API uses americas, asia, europe
        if self.region.lower() in ["na", "br", "latam", "oce", "la1", "la2", "na1", "br1", "oc1"]:
            return "americas"
        elif self.region.lower() in ["kr", "jp", "kr", "jp1"]:
            return "asia"
        else:  # eu, euw1, eun1, tr1, ru
            return "europe"
            
    async def get_player_puuid(self, riot_name: str, riot_tag: str) -> Optional[str]:
        """Get player PUUID from Riot API."""
        if not self.api_key:
            logger.warning("RIOT_API_KEY not set, cannot get player PUUID")
            return None
            
        try:
            account_region = self._get_account_region()
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
        
    async def get_summoner_id(self, puuid: str, region_override: Optional[str] = None) -> Optional[str]:
        """Get summoner ID from PUUID. Optionally try multiple regions if one fails."""
        if not self.api_key:
            return None
        
        # Try the configured region first
        regions_to_try = [region_override] if region_override else [self._get_lol_region()]
        
        # If original region was "ap", try common Asia Pacific regions
        if self.region.lower() == "ap" and not region_override:
            regions_to_try = ["kr", "jp1", "vn2", "ph2", "sg2", "th2", "tw2", "oc1"]
        
        for lol_region in regions_to_try:
            try:
                url = f"https://{lol_region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
                headers = {"X-Riot-Token": self.api_key}
                
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    summoner_id = data.get("id")
                    if summoner_id:
                        logger.info(f"Found summoner in region {lol_region}")
                        return summoner_id
                elif response.status_code == 404:
                    # Player not in this region, try next
                    continue
                elif response.status_code == 403:
                    error_data = response.json() if response.text else {}
                    error_msg = error_data.get("status", {}).get("message", "Forbidden")
                    
                    # If it's the first region and we get 403, log detailed error
                    if lol_region == regions_to_try[0]:
                        logger.error(
                            f"❌ 403 Forbidden when getting summoner ID in region '{lol_region}'.\n"
                            f"Possible causes:\n"
                            f"  1. API key expired or invalid - Check at https://developer.riotgames.com/\n"
                            f"  2. API key doesn't have League of Legends access\n"
                            f"  3. Region '{lol_region}' is incorrect for this player\n"
                            f"  4. Rate limit exceeded\n"
                            f"Error: {error_msg}\n"
                            f"💡 Tip: If you set RIOT_REGION=ap, try a specific region like 'kr', 'vn2', 'jp1', etc."
                        )
                    # Don't try other regions if it's a 403 (likely API key issue)
                    break
                else:
                    logger.warning(f"Unexpected status {response.status_code} for region {lol_region}: {response.text[:100]}")
                    
            except Exception as e:
                logger.error(f"Exception getting summoner ID from region {lol_region}: {str(e)}")
                continue
        
        return None
        
    async def get_current_match(self, summoner_id: str) -> Optional[Dict]:
        """Get current active match for a player."""
        if not self.api_key:
            return None
            
        try:
            lol_region = self._get_lol_region()
            url = f"https://{lol_region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}"
            headers = {"X-Riot-Token": self.api_key}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                # Player is not in a match
                return None
            elif response.status_code == 403:
                logger.warning("Riot API key may not have League of Legends API access.")
            else:
                logger.error(f"Error getting current match: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Exception getting current match: {str(e)}")
            
        return None
        
    async def get_recent_matches(self, puuid: str, count: int = 1) -> List[str]:
        """Get recent match IDs for a player."""
        if not self.api_key:
            return []
            
        try:
            account_region = self._get_account_region()
            url = f"https://{account_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
            headers = {"X-Riot-Token": self.api_key}
            params = {"start": 0, "count": count}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                logger.warning("Riot API key may not have League of Legends API access.")
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
            account_region = self._get_account_region()
            url = f"https://{account_region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
            headers = {"X-Riot-Token": self.api_key}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                logger.warning("Riot API key may not have League of Legends API access.")
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
                        # Get summoner ID
                        summoner_id = await self.get_summoner_id(puuid)
                        if summoner_id:
                            player_info["summoner_id"] = summoner_id
                    else:
                        continue
                else:
                    puuid = player_info["puuid"]
                
                # Get summoner ID if not cached
                if not player_info.get("summoner_id"):
                    summoner_id = await self.get_summoner_id(puuid)
                    if summoner_id:
                        player_info["summoner_id"] = summoner_id
                    else:
                        continue
                else:
                    summoner_id = player_info["summoner_id"]
                
                # First, try to get current active match
                current_match = await self.get_current_match(summoner_id)
                
                if current_match:
                    game_id = current_match.get("gameId")
                    was_in_match = player_info.get("in_match", False)
                    
                    # If player just entered a match
                    if not was_in_match:
                        player_info["in_match"] = True
                        player_info["current_match_id"] = str(game_id)
                        player_info["last_match_id"] = str(game_id)
                        new_matches.append({
                            "discord_user_id": discord_user_id,
                            "riot_name": riot_name,
                            "riot_tag": riot_tag,
                            "match_id": str(game_id),
                            "match_data": current_match,
                            "is_active": True
                        })
                        logger.info(f"New active match detected for {riot_name}#{riot_tag}: {game_id}")
                else:
                    # Player is not in a match anymore
                    was_in_match = player_info.get("in_match", False)
                    if was_in_match:
                        # Match just ended, get match details
                        player_info["in_match"] = False
                        # Get the most recent match from history
                        recent_match_ids = await self.get_recent_matches(puuid, count=1)
                        if recent_match_ids and len(recent_match_ids) > 0:
                            latest_match_id = recent_match_ids[0]
                            last_match_id = player_info.get("last_match_id")
                            
                            # Check if this is a new match
                            if latest_match_id != last_match_id:
                                # Get match details for stats
                                match_details = await self.get_match_details(latest_match_id)
                                if match_details:
                                    player_info["last_match_id"] = latest_match_id
                                    new_matches.append({
                                        "discord_user_id": discord_user_id,
                                        "riot_name": riot_name,
                                        "riot_tag": riot_tag,
                                        "match_id": latest_match_id,
                                        "match_data": match_details,
                                        "is_active": False,
                                        "match_ended": True
                                    })
                                    logger.info(f"Match ended for {riot_name}#{riot_tag}: {latest_match_id}")
                        player_info["current_match_id"] = None
                
            except Exception as e:
                logger.error(f"Error checking matches for player {discord_user_id}: {str(e)}")
                
        return new_matches
        
    async def start_monitoring(self, bot, check_interval: int = 30):
        """Start the background monitoring task."""
        if self.is_running:
            logger.warning("LoL monitoring is already running")
            return
            
        self.is_running = True
        self.check_interval = check_interval
        logger.info(f"Starting League of Legends match monitoring (interval: {check_interval}s)")
        
        # Initialize PUUIDs and summoner IDs for all tracked players
        for discord_user_id, player_info in self.tracked_players.items():
            if not player_info.get("puuid"):
                puuid = await self.get_player_puuid(
                    player_info["riot_name"],
                    player_info["riot_tag"]
                )
                if puuid:
                    player_info["puuid"] = puuid
                    summoner_id = await self.get_summoner_id(puuid)
                    if summoner_id:
                        player_info["summoner_id"] = summoner_id
                    
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
                                    f"đang trong trận đấu League of Legends!"
                                )
                                await channel.send(message)
                                logger.info(f"Sent notification for {match['riot_name']}#{match['riot_tag']} - LoL")
                            else:
                                message = (
                                    f"🎮 **{match['riot_name']}#{match['riot_tag']}** "
                                    f"đã bắt đầu một trận đấu League of Legends!"
                                )
                                await channel.send(message)
                                logger.info(f"Sent notification for {match['riot_name']}#{match['riot_tag']} - LoL")
                
                await asyncio.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"Error in LoL monitoring loop: {str(e)}")
                await asyncio.sleep(self.check_interval)
                
    async def send_match_end_notification(self, channel, match: Dict, bot):
        """Send match end notification with stats and AI comment."""
        try:
            from src.lol_match_stats import parse_player_stats, format_match_stats
            from src.lol_stats_comment import generate_match_comment
            
            player_info = self.tracked_players.get(match["discord_user_id"])
            if not player_info or not player_info.get("puuid"):
                return
            
            puuid = player_info["puuid"]
            match_data = match.get("match_data", {})
            
            # Parse stats
            stats = parse_player_stats(match_data, puuid)
            if not stats:
                await channel.send(
                    f"🎮 **{match['riot_name']}#{match['riot_tag']}** đã kết thúc trận đấu League of Legends!"
                )
                return
            
            # Format stats message
            stats_message = format_match_stats(stats, f"{match['riot_name']}#{match['riot_tag']}")
            
            # Generate AI comment
            ai_comment = await generate_match_comment(stats, f"{match['riot_name']}#{match['riot_tag']}")
            
            # Send combined message
            full_message = f"{stats_message}\n💬 **Nhận xét:** {ai_comment}"
            await channel.send(full_message)
            logger.info(f"Sent match end stats for {match['riot_name']}#{match['riot_tag']} - LoL")
            
        except Exception as e:
            logger.error(f"Error sending match end notification: {str(e)}")
            # Fallback to simple message
            try:
                await channel.send(
                    f"🎮 **{match['riot_name']}#{match['riot_tag']}** đã kết thúc trận đấu League of Legends!"
                )
            except:
                pass
    
    def stop_monitoring(self):
        """Stop the background monitoring task."""
        self.is_running = False
        logger.info("Stopped League of Legends match monitoring")

# Global tracker instance
lol_tracker = LeagueTracker()

