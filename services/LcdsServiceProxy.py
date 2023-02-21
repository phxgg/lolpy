from classes.league_client import LeagueClient
from classes.lcu_call import LCUCall


class LcdsServiceProxy:
    _service_name = 'lcdsServiceProxy'
    _league_client = None
    _lcu = None

    def __init__(self, league_client: LeagueClient):
        self._league_client = league_client
        self._lcu = LCUCall(self._league_client)

    def call(self, args: list) -> str:
        return self._lcu.invoke(self._service_name, 'call', args)
