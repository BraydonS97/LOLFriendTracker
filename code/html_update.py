from bs4 import BeautifulSoup
import math
import modules



def player_basic_banner(player_data):

    # Calculate win rate %
    total_games = player_data['wins'] / (player_data['wins'] + player_data['losses']) * 100

    # Check if the player is high enough elo to remove the Number part of the rank
    if player_data['tier'] == 'CHALLENGER' or player_data['tier'] == 'GRANDMASTER' or player_data['tier'] == 'MASTER':
        current_rank_info = player_data['tier'] + " - " + "{:,}".format(player_data['leaguePoints']) + " LP"
    else: 
        current_rank_info = player_data['tier'] + " " + player_data['rank'] + " - " + str(player_data['leaguePoints']) + " LP"
    # print(player_data)
    player_banner_mapping = {
        "SUMMONER_NAME": player_data['gameName'],
        "CURRENT_RANK": current_rank_info,
        "TOTAL_WINS_NUMBER": str(player_data['wins']),
        "TOTAL_LOSSES_NUMBER": str(player_data['losses']),
        "WINRATE_NUMBER": str(math.trunc(total_games)) + "%",
    }

    modules.html_div_changer(player_banner_mapping)

def player_game_status_banner(player_data, player_game_data):

    game_info_mapping = {}

    if player_game_data[2] == "IN GAME":

        # Current Game Mapping
        participants = player_game_data[0]['participants']

        for participant in participants:
            if participant['puuid'] == player_data['puuid']:
                game_info_mapping = {
                    "CHAMPION_ICON": modules.get_champion_img(str(participant['championId'])),
                    "SUMMONER_ICON1": modules.get_summoner_spell_img(str(participant['spell1Id'])),
                    "SUMMONER_ICON2": modules.get_summoner_spell_img(str(participant['spell2Id']))
                }

        player_game_status_mapping = {
            "GAME_STATUS": player_game_data[2],
            "GAME_STATUS_TIMER": modules.format_game_time(player_game_data[0]['gameStartTime']),
            "current-game-status": "Playing Now",
            "GAMES_PLAYED": player_game_data[1]
        }
    else:
        game_info_mapping = {
            "CHAMPION_ICON": '',
            "SUMMONER_ICON1": '',
            "SUMMONER_ICON2": '',
        }

        player_game_status_mapping = {
            "GAME_STATUS": player_game_data[2],
            "GAME_STATUS_TIMER": player_game_data[0][0],
            "current-game-status": "Last Played",
            "GAMES_PLAYED": player_game_data[1]
        }

    modules.html_div_changer(player_game_status_mapping)
    modules.html_div_changer(game_info_mapping) 
