import requests
import json

from .league_client import LeagueClient

class RiotCall:
    _league_client = None
    _url = None
    _headers = None

    def __init__(self, league_client: LeagueClient) -> None:
        self._league_client = league_client
        self._url = f'https://127.0.0.1:{self._league_client.get_riot_port()}'
        self.set_headers()

    def set_headers(self) -> None:
        '''
        Set headers for requests.
        '''
        self._headers = {
            'Content-Type': 'application/json',
			'Accept': 'application/json',
			'User-Agent': 'LeagueOfLegendsClient',
			'Authorization': 'Basic ' + self._league_client.get_riot_session_token()
        }

    def get(self, path: str) -> str:
        r = requests.get(f'{self._url}{path}', headers=self._headers, verify=False)
        return json.loads(r.text)
    
    def post(self, path: str, data: str) -> str:
        r = requests.post(f'{self._url}{path}', headers=self._headers, data=data, verify=False)
        return json.loads(r.text)
    
    def put(self, path: str, data: str) -> str:
        r = requests.put(f'{self._url}{path}', headers=self._headers, data=data, verify=False)
        return json.loads(r.text)
    
    def delete(self, path: str) -> str:
        r = requests.delete(f'{self._url}{path}', headers=self._headers, verify=False)
        return json.loads(r.text)

    

