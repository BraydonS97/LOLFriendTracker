from bs4 import BeautifulSoup
import math
import shutil
import modules

def player_banner_update(player_data, player_game_status):
    with open('index.html', 'r') as file:
        html_content = file.read()

    # Calculate win rate
    total_games = player_data['wins'] / (player_data['wins'] + player_data['losses']) * 100

    # Check if the player is high enough elo to remove the Number part of the rank
    if player_data['tier'] == 'CHALLENGER' or player_data['tier'] == 'GRANDMASTER' or player_data['tier'] == 'MASTER':
        current_rank_info = player_data['tier'] + " - " + "{:,}".format(player_data['leaguePoints']) + " LP"
    else: 
        current_rank_info = player_data['tier'] + " " + player_data['rank'] + " - " + str(player_data['leaguePoints']) + " LP"

    player_info_mapping = {}
    game_info_mapping = {}
    # Define a dictionary to map class names to new content
    # print(player_game_status)
    if player_game_status[1] == "IN GAME":

        # Current Game Mapping
        participants = player_game_status[0]['participants']

        for participant in participants:
            if participant['puuid'] == player_data['puuid']:
                game_info_mapping = {
                    "CHAMPION_ICON": modules.get_champion_img(str(participant['championId'])),
                    "SUMMONER_ICON1": modules.get_summoner_spell_img(str(participant['spell1Id'])),
                    "SUMMONER_ICON2": modules.get_summoner_spell_img(str(participant['spell2Id']))
                }

        # Basic player info Mapping
        player_info_mapping = {
            "SUMMONER_NAME": player_data['gameName'],
            "CURRENT_RANK": current_rank_info,
            "TOTAL_WINS_NUMBER": str(player_data['wins']),
            "TOTAL_LOSSES_NUMBER": str(player_data['losses']),
            "WINRATE_NUMBER": str(math.trunc(total_games)) + "%",
            "GAME_STATUS": player_game_status[1],
            "GAME_STATUS_TIMER": modules.format_game_time(player_game_status[0]['gameStartTime']),
            "current-game-status": "Game Length",
            "GAMES_PLAYED": player_data['games_played_today']

        }
    else:
        # print(player_game_status)
        game_info_mapping = {
            "CHAMPION_ICON": '',
            "SUMMONER_ICON1": '',
            "SUMMONER_ICON2": '',
        }
        player_info_mapping = {
            "SUMMONER_NAME": player_data['gameName'],
            "CURRENT_RANK": current_rank_info,
            "TOTAL_WINS_NUMBER": str(player_data['wins']),
            "TOTAL_LOSSES_NUMBER": str(player_data['losses']),
            "WINRATE_NUMBER": str(math.trunc(total_games)) + "%",
            "GAME_STATUS": player_game_status[1],
            "GAME_STATUS_TIMER": player_game_status[0][0],
            "current-game-status": "Last Played",
            "GAMES_PLAYED": player_data['games_played_today']
        }

    player_info_mapping.update(game_info_mapping)
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find and modify <div> elements based on the class name mapping
    for class_name, new_content in player_info_mapping.items():
        div_element = soup.find('div', class_=class_name)

        if div_element:
            img_element = div_element.find('img')
            if img_element:
                img_element['src'] = new_content
            else:
                div_element.string = new_content
        else:
            print(f"No <div> element found with class name: {class_name}")

    # Save the modified HTML content to a temporary file
    with open('modified_index.html', 'w') as file:
        file.write(str(soup))

    # Replace the original file with the modified one
    shutil.move('modified_index.html', 'index.html')