import requests
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Player:
    account_id: int
    personaname: str
    name: Optional[str] = None
    avatar: Optional[str] = None
    avatarmedium: Optional[str] = None
    avatarfull: Optional[str] = None
    profileurl: Optional[str] = None
    last_login: Optional[datetime] = None
    loccountrycode: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Player':
        return cls(
            account_id=data.get('account_id', 0),
            personaname=data.get('profile', {}).get('personaname', ''),
            name=data.get('profile', {}).get('name'),
            avatar=data.get('profile', {}).get('avatar'),
            avatarmedium=data.get('profile', {}).get('avatarmedium'),
            avatarfull=data.get('profile', {}).get('avatarfull'),
            profileurl=data.get('profile', {}).get('profileurl'),
            last_login=datetime.fromtimestamp(data['profile']['last_login']) if data.get('profile', {}).get('last_login') else None,
            loccountrycode=data.get('profile', {}).get('loccountrycode')
        )


@dataclass
class Match:
    match_id: int
    duration: int
    start_time: datetime
    radiant_win: bool
    game_mode: int
    lobby_type: int
    human_players: int
    players: List[Dict[str, Any]] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Match':
        return cls(
            match_id=data['match_id'],
            duration=data.get('duration', 0),
            start_time=datetime.fromtimestamp(data['start_time']),
            radiant_win=data.get('radiant_win', False),
            game_mode=data.get('game_mode', 0),
            lobby_type=data.get('lobby_type', 0),
            human_players=data.get('human_players', 0),
            players=data.get('players', [])
        )


@dataclass
class Hero:
    id: int
    name: str
    localized_name: str
    primary_attr: str
    attack_type: str
    roles: List[str] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Hero':
        return cls(
            id=data['id'],
            name=data['name'],
            localized_name=data['localized_name'],
            primary_attr=data['primary_attr'],
            attack_type=data['attack_type'],
            roles=data.get('roles', [])
        )


@dataclass
class PlayerMatch:
    match_id: int
    player_slot: int
    radiant_win: bool
    duration: int
    game_mode: int
    lobby_type: int
    hero_id: int
    start_time: datetime
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PlayerMatch':
        return cls(
            match_id=data['match_id'],
            player_slot=data.get('player_slot', 0),
            radiant_win=data.get('radiant_win', False),
            duration=data.get('duration', 0),
            game_mode=data.get('game_mode', 0),
            lobby_type=data.get('lobby_type', 0),
            hero_id=data.get('hero_id', 0),
            start_time=datetime.fromtimestamp(data['start_time']),
            kills=data.get('kills', 0),
            deaths=data.get('deaths', 0),
            assists=data.get('assists', 0)
        )


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
    def get_player(self, account_id: int) -> Player:
        """Get player data"""
        data = self._request(f"players/{account_id}")
        return Player.from_dict(data)
    
    def get_player_matches(self, account_id: int, limit: int = 20, **kwargs) -> List[PlayerMatch]:
        """Get player matches"""
        params = {"limit": limit, **kwargs}
        data = self._request(f"players/{account_id}/matches", params)
        return [PlayerMatch.from_dict(match) for match in data]
    
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
    def get_match(self, match_id: int) -> Match:
        """Get match details"""
        data = self._request(f"matches/{match_id}")
        return Match.from_dict(data)
    
    def get_public_matches(self, **kwargs) -> List[Dict[str, Any]]:
        """Get public matches"""
        return self._request("publicMatches", kwargs)
    
    def get_parsed_matches(self, **kwargs) -> List[Dict[str, Any]]:
        """Get parsed matches"""
        return self._request("parsedMatches", kwargs)
    
    # Heroes endpoints
    def get_heroes(self) -> List[Hero]:
        """Get heroes list"""
        data = self._request("heroes")
        return [Hero.from_dict(hero) for hero in data]
    
    def get_hero_matches(self, hero_id: int) -> List[Dict[str, Any]]:
        """Get hero matches"""
        return self._request(f"heroes/{hero_id}/matches")
    
    def get_hero_matchups(self, hero_id: int) -> List[Dict[str, Any]]:
        """Get hero matchups"""
        return self._request(f"heroes/{hero_id}/matchups")
    
    def get_hero_durations(self, hero_id: int) -> List[Dict[str, Any]]:
        """Get hero performance over a range of match durations"""
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