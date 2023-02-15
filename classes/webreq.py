import requests


class WebReq:
    '''
    Used to perform HTTP requests to Riot's actual API.
    '''
    def __init__(self, content_type: str, accept: str, access_token: str, user_agent: str) -> None:
        if not access_token:
            raise ValueError('access_token is required')

        if not content_type:
            content_type = 'application/json'

        if not accept:
            accept = 'application/json'

        if not user_agent:
            user_agent = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) LeagueOfLegendsClient/13.3.491.0715 (CEF 91) Safari/537.36'

        self._session = requests.Session()
        self._session.verify = False
        self._session.headers = {
            'Content-Type': content_type,
            'Accept': accept,
            'Authorization': f'Bearer {access_token}',
            'User-Agent': user_agent,
            'Accept-Encoding': 'deflate, gzip, zstd',
        }

    def get(self, url: str) -> str:
        return self._session.get(url).json()

    def post(self, url: str, json: str) -> str:
        return self._session.post(url, json=json).json()

    def put(self, url: str, json: str) -> str:
        return self._session.put(url, json=json).json()
