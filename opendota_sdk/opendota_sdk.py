import requests
from typing import Optional, Dict, Any, List


class OpenDotaClient:
    """Professional OpenDota API client"""
    
    BASE_URL = "https://api.opendota.com/api"
    
    def __init__(self, api_key: Optional[str] = None, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'OpenDota-Python-SDK/1.0',
            'Accept': 'application/json'
        })
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    def _request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute API request with error handling"""
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            raise OpenDotaAPIError("Request timeout")
        except requests.HTTPError as e:
            raise OpenDotaAPIError(f"HTTP {e.response.status_code}: {e.response.text}")
        except requests.RequestException as e:
            raise OpenDotaAPIError(f"Request failed: {e}")
        except ValueError as e:
            raise OpenDotaAPIError(f"Invalid JSON response: {e}")
    
    # Player endpoints
    def get_player(self, account_id: int) -> Dict[str, Any]:
        """Get player data"""
        return self._request(f"players/{account_id}")
    
    def get_player_matches(self, account_id: int, limit: int = 20, **kwargs) -> List[Dict[str, Any]]:
        """Get player matches"""
        params = {"limit": limit, **kwargs}
        return self._request(f"players/{account_id}/matches", params)
    
    def get_player_heroes(self, account_id: int) -> List[Dict[str, Any]]:
        """Get player hero statistics"""
        return self._request(f"players/{account_id}/heroes")
    
    def get_player_peers(self, account_id: int) -> List[Dict[str, Any]]:
        """Get player peers"""
        return self._request(f"players/{account_id}/peers")
    
    def get_player_pros(self, account_id: int) -> List[Dict[str, Any]]:
        """Get pro players played with"""
        return self._request(f"players/{account_id}/pros")
    
    def get_player_totals(self, account_id: int) -> List[Dict[str, Any]]:
        """Get player totals"""
        return self._request(f"players/{account_id}/totals")
    
    def get_player_counts(self, account_id: int) -> Dict[str, Any]:
        """Get player counts"""
        return self._request(f"players/{account_id}/counts")
    
    def get_player_histograms(self, account_id: int, field: str) -> List[Dict[str, Any]]:
        """Get player histograms"""
        params = {"field": field}
        return self._request(f"players/{account_id}/histograms", params)
    
    def get_player_wardmap(self, account_id: int) -> Dict[str, Any]:
        """Get player ward map"""
        return self._request(f"players/{account_id}/wardmap")
    
    def get_player_wordcloud(self, account_id: int) -> Dict[str, Any]:
        """Get player word cloud"""
        return self._request(f"players/{account_id}/wordcloud")
    
    def get_player_ratings(self, account_id: int) -> List[Dict[str, Any]]:
        """Get player ratings"""
        return self._request(f"players/{account_id}/ratings")
    
    def get_player_rankings(self, account_id: int) -> List[Dict[str, Any]]:
        """Get player rankings"""
        return self._request(f"players/{account_id}/rankings")
    
    # Match endpoints
    def get_match(self, match_id: int) -> Dict[str, Any]:
        """Get match details"""
        return self._request(f"matches/{match_id}")
    
    def get_public_matches(self, **kwargs) -> List[Dict[str, Any]]:
        """Get public matches"""
        return self._request("publicMatches", kwargs)
    
    def get_parsed_matches(self, **kwargs) -> List[Dict[str, Any]]:
        """Get parsed matches"""
        return self._request("parsedMatches", kwargs)
    
    # Heroes endpoints
    def get_heroes(self) -> List[Dict[str, Any]]:
        """Get heroes list"""
        return self._request("heroes")
    
    def get_hero_matches(self, hero_id: int) -> List[Dict[str, Any]]:
        """Get hero matches"""
        return self._request(f"heroes/{hero_id}/matches")
    
    def get_hero_matchups(self, hero_id: int) -> List[Dict[str, Any]]:
        """Get hero matchups"""
        return self._request(f"heroes/{hero_id}/matchups")
    
    def get_hero_durations(self, hero_id: int) -> List[Dict[str, Any]]:
        """Get hero durations"""
        return self._request(f"heroes/{hero_id}/durations")
    
    def get_hero_players(self, hero_id: int) -> List[Dict[str, Any]]:
        """Get hero players"""
        return self._request(f"heroes/{hero_id}/players")
    
    def get_hero_stats(self) -> List[Dict[str, Any]]:
        """Get hero stats"""
        return self._request("heroStats")
    
    # Pro matches endpoints
    def get_pro_matches(self, **kwargs) -> List[Dict[str, Any]]:
        """Get pro matches"""
        return self._request("proMatches", kwargs)
    
    def get_pro_players(self) -> List[Dict[str, Any]]:
        """Get pro players"""
        return self._request("proPlayers")
    
    def get_teams(self) -> List[Dict[str, Any]]:
        """Get teams"""
        return self._request("teams")
    
    def get_team(self, team_id: int) -> Dict[str, Any]:
        """Get team details"""
        return self._request(f"teams/{team_id}")
    
    def get_team_matches(self, team_id: int) -> List[Dict[str, Any]]:
        """Get team matches"""
        return self._request(f"teams/{team_id}/matches")
    
    def get_team_players(self, team_id: int) -> List[Dict[str, Any]]:
        """Get team players"""
        return self._request(f"teams/{team_id}/players")
    
    def get_team_heroes(self, team_id: int) -> List[Dict[str, Any]]:
        """Get team heroes"""
        return self._request(f"teams/{team_id}/heroes")
    
    # League endpoints
    def get_leagues(self) -> List[Dict[str, Any]]:
        """Get leagues"""
        return self._request("leagues")
    
    def get_league(self, league_id: int) -> Dict[str, Any]:
        """Get league details"""
        return self._request(f"leagues/{league_id}")
    
    def get_league_matches(self, league_id: int) -> List[Dict[str, Any]]:
        """Get league matches"""
        return self._request(f"leagues/{league_id}/matches")
    
    def get_league_teams(self, league_id: int) -> List[Dict[str, Any]]:
        """Get league teams"""
        return self._request(f"leagues/{league_id}/teams")
    
    # Search and other endpoints
    def search_players(self, query: str) -> List[Dict[str, Any]]:
        """Search players"""
        params = {"q": query}
        return self._request("search", params)
    
    def get_rankings(self, hero_id: str) -> List[Dict[str, Any]]:
        """Get rankings"""
        return self._request(f"rankings", {"hero_id": hero_id})
    
    def get_benchmarks(self, hero_id: int) -> Dict[str, Any]:
        """Get benchmarks"""
        return self._request(f"benchmarks", {"hero_id": hero_id})
    
    def get_status(self) -> Dict[str, Any]:
        """Get API status"""
        return self._request("status")
    
    def get_health(self) -> Dict[str, Any]:
        """Get API health"""
        return self._request("health")
    
    def get_request(self, job_id: str) -> Dict[str, Any]:
        """Get request status"""
        return self._request(f"request/{job_id}")
    
    def post_request(self, match_id: int) -> Dict[str, Any]:
        """Request match parse"""
        try:
            response = self.session.post(
                f"{self.BASE_URL}/request/{match_id}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise OpenDotaAPIError(f"Request failed: {e}")


class OpenDotaAPIError(Exception):
    """OpenDota API exception"""
    pass