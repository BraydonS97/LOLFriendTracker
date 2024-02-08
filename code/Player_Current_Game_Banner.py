from bs4 import BeautifulSoup
import json
import shutil
from datetime import datetime, timedelta


json_file_path = r'/json_files/summoner.json'
    
def get_id_from_key(json_file_path, key_to_find):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    matching_objects = []
    if 'data' in data:
        for entry in data['data'].values():
            if 'key' in entry and entry['key'] == key_to_find:
                matching_objects.append(entry)
    
    for obj in matching_objects:
        return "/images/SummonerSpells/" + str(obj['id'] + ".png")
    
    
def format_game_time(game_start_time):
    start_time = datetime.fromtimestamp(game_start_time / 1000) + timedelta(seconds=30)

    current_time = datetime.now()
    time_difference = current_time - start_time

    total_seconds = time_difference.total_seconds()

    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)

    time_string = "{:02d}:{:02d}".format(minutes, seconds)
    
    return str(time_string)
    


def update_game_banner(game_data, player_data):
    # Read the HTML file
    with open('index.html', 'r') as file:
        html_content = file.read()

    class_mapping = {}

    # print(game_data[0])
    if game_data[1] == "IN GAME":

        participants = game_data[0]['participants']
        for participant in participants:
            if participant['puuid'] == player_data['puuid']:
                class_mapping = {
                    "SUMMONER_ICON1": get_id_from_key(json_file_path, str(participant['spell1Id'])),
                    "SUMMONER_ICON2": get_id_from_key(json_file_path, str(participant['spell2Id'])),
                    # "GAME_STATUS_TIMER": format_game_time(game_data[0]['gameStartTime'])
                    # "SUMMONER_RUNE1": participant['perkStyle'],
                    # "SUMMONER_RUNE2": participant['perkSubStyle']
                }
    else:
        class_mapping = {
                    "SUMMONER_ICON1": "",
                    "SUMMONER_ICON2": "",
                    "GAME_STATUS_TIMER": "000"
                }
        pass

    # # Define a dictionary to map class names to new content

    # # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # # Find and modify <div> elements based on the class name mapping
    for class_name, new_content in class_mapping.items():
        div_element = soup.find('div', class_=class_name)

        if div_element:
            img_element = div_element.find('img')
            if img_element:
                img_element['src'] = new_content
            else:
                div_element.string = new_content



    # # Save the modified HTML content to a temporary file
    with open('modified_index.html', 'w') as file:
        file.write(str(soup))

    # # Replace the original file with the modified one
    shutil.move('modified_index.html', 'index.html')
