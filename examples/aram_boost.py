from urllib3 import disable_warnings

from classes.league_client import LeagueClient
from classes.lcu_call import LCUCall
from classes.riot_call import RiotCall
from services.LcdsServiceProxy import LcdsServiceProxy

# suppress warnings
# requests.packages.urllib3.disable_warnings()
disable_warnings()


def main():
    league_client = LeagueClient()

    lcu = LCUCall(league_client)
    riot = RiotCall(league_client)

    lcdsServiceProxy = LcdsServiceProxy(league_client)

    current_summoner = lcu.get_current_summoner()
    print(f'Connected: {current_summoner["displayName"]}')
    print(f'Puuid: {current_summoner["puuid"]}')

    print(f'LCU: https://127.0.0.1:{league_client.get_lcu_port()}')
    print(f'Riot: https://127.0.0.1:{league_client.get_riot_port()}')

    # Aram Boost
    r = lcdsServiceProxy.call(["", "teambuilder-draft", "activateBattleBoostV1", ""])
    print(r)


if __name__ == '__main__':
    main()
