from bs4 import BeautifulSoup
import math
import shutil
import modules

def player_banner_update(player_data, player_game_status):
    with open('index.html', 'r') as file:
        html_content = file.read()

    # Calculate win rate
    total_games = player_data['wins'] / (player_data['wins'] + player_data['losses']) * 100
    print("TEST:", player_data['leaguePoints'])
    # Check if the player is high enough elo to remove the Number part of the rank
    if player_data['tier'] == 'CHALLENGER' or player_data['tier'] == 'GRANDMASTER' or player_data['tier'] == 'MASTER':
        current_rank_info = player_data['tier'] + " - " + "{:,}".format(player_data['leaguePoints']) + " LP"
    else: 
        current_rank_info = player_data['tier'] + " " + player_data['rank'] + " - " + str(player_data['leaguePoints']) + " LP"

    class_mapping = {}
    # Define a dictionary to map class names to new content
    if player_game_status[1] == "IN GAME":
        class_mapping = {
            "SUMMONER_NAME": player_data['gameName'],
            "CURRENT_RANK": current_rank_info,
            "TOTAL_WINS_NUMBER": str(player_data['wins']),
            "TOTAL_LOSSES_NUMBER": str(player_data['losses']),
            "WINRATE_NUMBER": str(math.trunc(total_games)) + "%",
            "GAME_STATUS": player_game_status[1],
            "GAME_STATUS_TIMER": modules.format_game_time(player_game_status[0]['gameStartTime'])
        }
    else:
        pass

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find and modify <div> elements based on the class name mapping
    for class_name, new_content in class_mapping.items():
        div_element = soup.find('div', class_=class_name)
        if div_element:
            div_element.string = new_content
        else:
            print(f"No <div> element found with class name: {class_name}")

    # Save the modified HTML content to a temporary file
    with open('modified_index.html', 'w') as file:
        file.write(str(soup))

    # Replace the original file with the modified one
    shutil.move('modified_index.html', 'index.html')