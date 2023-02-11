import random
from urllib3 import disable_warnings
import json

from classes.league_client import LeagueClient
from classes.lcu_call import LCUCall
from classes.riot_call import RiotCall

# suppress warnings
# requests.packages.urllib3.disable_warnings()
disable_warnings()

def main():
	league_client = LeagueClient()

	lcu = LCUCall(league_client)
	riot = RiotCall(league_client)

	current_summoner = lcu.get_current_summoner()
	print(f'Connected: {current_summoner["displayName"]}')

	print(f'LCU: https://127.0.0.1:{league_client.get_lcu_port()}')
	print(f'Riot: https://127.0.0.1:{league_client.get_riot_port()}')

	victim = lcu.get_summoner_by_name('Haver Volren')

	print(f'Name: {victim["displayName"]}')
	print(f'Summoner ID: {victim["summonerId"]}')

	# Reporting the player more than once will return an error: "Account was already reported."
	# However, if you logout and login again, you can report the same player again.
	# Also it seems like we can use any random number for the gameId.
	for i in range(2):
		GAME_ID = random.randint(3000000000, 3313105043)

		report = lcu.send_report(data=json.dumps({
			'comment': '',
			'gameId': GAME_ID,
			'offenses': 'NEGATIVE_ATTITUDE,VERBAL_ABUSE,THIRD_PARTY_TOOLS',
			'reportedSummonerId': victim['summonerId'],
		}))

		print(report)


if __name__ == '__main__':
	main()
