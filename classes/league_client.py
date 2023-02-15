import sys
import platform
import psutil
import base64


class LeagueClient():
    _lcu_name = None

    _lcu_token = None
    _lcu_port = None
    _lcu_session = None

    _riot_token = None
    _riot_port = None
    _riot_session = None

    _region = None

    def __init__(self):
        self.set_lcu_name()
        self.set_lcu_arguments()
        self.set_sessions()

    def lcu_available(self) -> bool:
        '''
        Check whether a client is available.
        '''
        return self._lcu_name in (p.name() for p in psutil.process_iter())

    def set_lcu_name(self) -> None:
        '''
        Set LeagueClient executable name depending on platform.
        '''
        if platform.system() == 'Windows':
            self._lcu_name = 'LeagueClientUx.exe'
        elif platform.system() == 'Darwin':
            self._lcu_name = 'LeagueClientUx'
        elif platform.system() == 'Linux':
            self._lcu_name = 'LeagueClientUx'

    def set_lcu_arguments(self) -> None:
        '''
        Set region, remoting-auth-token and app-port for LeagueClientUx.
        '''
        if not self.lcu_available():
            sys.exit('No ' + self._lcu_name +
                     ' found. Login to an account and try again.')

        for p in psutil.process_iter():
            if p.name() == self._lcu_name:
                args = p.cmdline()

                for a in args:
                    if '--region=' in a:
                        self._region = a.split('--region=', 1)[1].lower()
                    if '--remoting-auth-token=' in a:
                        self._lcu_token = a.split('--remoting-auth-token=', 1)[1]
                    if '--app-port' in a:
                        self._lcu_port = a.split('--app-port=', 1)[1]
                    if '--riotclient-auth-token=' in a:
                        self._riot_token = a.split('--riotclient-auth-token=', 1)[1]
                    if '--riotclient-app-port=' in a:
                        self._riot_port = a.split('--riotclient-app-port=', 1)[1]

    def set_sessions(self) -> None:
        '''
        Set requests sessions for LCU and RiotClient.
        '''
        self._lcu_session = base64.b64encode(
            f'riot:{self._lcu_token}'.encode('ascii')).decode('ascii')
        self._riot_session = base64.b64encode(
            f'riot:{self._riot_token}'.encode('ascii')).decode('ascii')

    def get_lcu_name(self) -> str:
        '''
        Get LeagueClient executable name.
        '''
        return self._lcu_name

    def get_lcu_token(self) -> str:
        '''
        Get LCU auth token.
        '''
        return self._lcu_token

    def get_lcu_port(self) -> str:
        '''
        Get LCU app port.
        '''
        return self._lcu_port

    def get_lcu_session_token(self) -> str:
        '''
        Get LCU session token.
        '''
        return self._lcu_session

    def get_riot_token(self) -> str:
        '''
        Get RiotClient auth token.
        '''
        return self._riot_token

    def get_riot_port(self) -> str:
        '''
        Get RiotClient app port.
        '''
        return self._riot_port

    def get_riot_session_token(self) -> str:
        '''
        Get RiotClient session token.
        '''
        return self._riot_session

    def get_region(self) -> str:
        '''
        Get region.
        '''
        return self._region
