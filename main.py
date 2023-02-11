import sys
import requests
from urllib3 import disable_warnings
import json
from time import sleep
import platform
import psutil
import base64
from os import system, name

# suppress warnings
# requests.packages.urllib3.disable_warnings()
disable_warnings()

# global variables
app_port = None
auth_token = None
riotclient_auth_token = None
riotclient_app_port = None
region = None
lcu_name = None  # LeagueClientUx executable name

# functions
def getLCUName():
    '''
    Get LeagueClient executable name depending on platform.
    '''
    global lcu_name
    if platform.system() == 'Windows':
        lcu_name = 'LeagueClientUx.exe'
    elif platform.system() == 'Darwin':
        lcu_name = 'LeagueClientUx'
    elif platform.system() == 'Linux':
        lcu_name = 'LeagueClientUx'


def LCUAvailable():
    '''
    Check whether a client is available.
    '''
    return lcu_name in (p.name() for p in psutil.process_iter())


def getLCUArguments():
    global auth_token, app_port, region, riotclient_auth_token, riotclient_app_port
    '''
    Get region, remoting-auth-token and app-port for LeagueClientUx.
    '''
    if not LCUAvailable():
        sys.exit('No ' + lcu_name + ' found. Login to an account and try again.')

    for p in psutil.process_iter():
        if p.name() == lcu_name:
            args = p.cmdline()

            for a in args:
                if '--region=' in a:
                    region = a.split('--region=', 1)[1].lower()
                if '--remoting-auth-token=' in a:
                    auth_token = a.split('--remoting-auth-token=', 1)[1]
                if '--app-port' in a:
                    app_port = a.split('--app-port=', 1)[1]
                if '--riotclient-auth-token=' in a:
                    riotclient_auth_token = a.split('--riotclient-auth-token=', 1)[1]
                if '--riotclient-app-port=' in a:
                    riotclient_app_port = a.split('--riotclient-app-port=', 1)[1]


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def main():
    # get LeagueClient name
    getLCUName()

    # get app port & auth token for each client
    getLCUArguments()

    lcu_api = 'https://127.0.0.1:' + app_port
    riotclient_api = 'https://127.0.0.1:' + riotclient_app_port

    lcu_session_token = base64.b64encode(
        ('riot:' + auth_token).encode('ascii')).decode('ascii')

    riotclient_session_token = base64.b64encode(
        ('riot:' + riotclient_auth_token).encode('ascii')).decode('ascii')

    lcu_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Basic ' + lcu_session_token
    }

    riotclient_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'LeagueOfLegendsClient',
        'Authorization': 'Basic ' + riotclient_session_token
    }

    # get current summoner
    get_current_summoner = lcu_api + '/lol-summoner/v1/current-summoner'

    r = requests.get(get_current_summoner, headers=lcu_headers, verify=False)
    r = json.loads(r.text)

    print('Connected: ' + r['displayName'])

    print(f'{lcu_api}')
    print(f'{auth_token}')

    VICTIM = 'Haver Volren'
    GAME_ID = 3313105043

    r = requests.get(lcu_api + f'/lol-summoner/v1/summoners?name={requests.utils.quote(VICTIM)}', headers=lcu_headers, verify=False)
    r = json.loads(r.text)

    summonerId = r['summonerId']

    print(f'Name: {r["displayName"]}')
    print(f'Summoner ID: {r["summonerId"]}')
    print(f'Puuid: {r["puuid"]}')

    # Reporting the player more than once will return an error: "Account was already reported."
    # However, if you logout and login again, you can report the same player again.
    # Also it seems like we can use any random number for the gameId.
    for i in range(2):
      r = requests.post(lcu_api + '/lol-end-of-game/v2/player-complaints', headers=lcu_headers, verify=False, data=json.dumps({
          "comment": "",
          "gameId": GAME_ID,
          "offenses": "NEGATIVE_ATTITUDE,VERBAL_ABUSE,THIRD_PARTY_TOOLS",
          "reportedSummonerId": summonerId,
      }))
      
      print(r.text)


if __name__ == '__main__':
    main()
