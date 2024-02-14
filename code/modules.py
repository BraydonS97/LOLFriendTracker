import requests
import time
import json
import os
import pytz
import shutil

from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup

def html_div_changer(mapped_data):
    with open('index.html', 'r') as file:
            html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find and modify <div> elements based on the class name mapping
    for class_name, new_content in mapped_data.items():
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



def get_champion_img(key_to_find):
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.dirname(current_directory)
    file_path = os.path.join(parent_directory, "json_files", "champion_id.json")

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    matching_objects = []
    if 'data' in data:
        for entry in data['data'].values():
            if 'key' in entry and entry['key'] == key_to_find:
                matching_objects.append(entry)
    
    for obj in matching_objects:
        return "/images/ChampionIcons/" + str(obj['id'] + "_0.jpg")

def games_played_today(summoner_puuid, api_key):

    # Get today's date in local time
    local_timezone = pytz.timezone('America/New_York')
    today_local = datetime.now(local_timezone).date()

    # Get the start of the day
    start_of_day_local = local_timezone.localize(datetime.combine(today_local, datetime.min.time()))
    # print(start_of_day_local)

    # Get the end of the day
    end_of_day_local = local_timezone.localize(datetime.combine(today_local, datetime.max.time()))

    # Convert to epoch timestamps
    start_epoch_local = int(start_of_day_local.timestamp())
    # print(start_epoch_local)
    end_epoch_local = int(end_of_day_local.timestamp())
    # print(end_epoch_local)

    player_matches_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{summoner_puuid['puuid']}/ids?startTime={start_epoch_local}&endTime={end_epoch_local}&type=ranked&start=0&count=40&api_key={api_key}"
    
    response = requests.get(player_matches_url)
    if response.status_code == 200:
        player_game_status = response.json()
        return str(len(player_game_status))
    else:
        print("Failed to retrieve data:", response.text)
        



    
def get_summoner_spell_img(key_to_find):
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.dirname(current_directory)
    file_path = os.path.join(parent_directory, "json_files", "summoner_spellid.json")

    with open(file_path, 'r') as file:
        data = json.load(file)
    
    matching_objects = []
    if 'data' in data:
        for entry in data['data'].values():
            if 'key' in entry and entry['key'] == key_to_find:
                matching_objects.append(entry)
    
    for obj in matching_objects:
        return "/images/SummonerSpells/" + str(obj['id'] + ".png")
    

def last_match(last_match_data):

    match_start_time = last_match_data['info']['gameStartTimestamp'] / 1000
    game_duration = last_match_data['info']['gameDuration']

    current_time = time.time()

    time_difference = current_time - (match_start_time + game_duration)
    
    if time_difference < 60:  # Less than a minute
        return f"{int(time_difference)} seconds ago", last_match_data
    elif time_difference < 3600:  # Less than an hour
        minutes = int(time_difference / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago", last_match_data
    elif time_difference < 86400:  # Less than a day
        hours = int(time_difference / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago", last_match_data
    elif time_difference < 2592000:  # Less than a month (30 days)
        days = int(time_difference / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago", last_match_data
    else:  # More than a month
        months = int(time_difference) // (30 * 86400)
        return f"{months} month{'s' if months != 1 else ''} ago", last_match_data
    

def time_since_last_match(player_last_match, api_key):
    try:
        player_match_data = f'https://americas.api.riotgames.com/lol/match/v5/matches/{player_last_match}?api_key={api_key}'
        response = requests.get(player_match_data)

        if response.status_code == 200:
            player_specific_match = response.json()

            match_start_time = player_specific_match['info']['gameStartTimestamp'] / 1000
            game_duration = player_specific_match['info']['gameDuration']

            current_time = time.time()

            time_difference = current_time - (match_start_time + game_duration)

        # Player_speicifc_match retursn the last game data in full.

        if time_difference < 60:  # Less than a minute
            return f"{int(time_difference)} seconds ago", player_specific_match
        elif time_difference < 3600:  # Less than an hour
            minutes = int(time_difference / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago", player_specific_match
        elif time_difference < 86400:  # Less than a day
            hours = int(time_difference / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago", player_specific_match
        elif time_difference < 2592000:  # Less than a month (30 days)
            days = int(time_difference / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago", player_specific_match
        else:  # More than a month
            months = int(time_difference) // (30 * 86400)
            return f"{months} month{'s' if months != 1 else ''} ago", player_specific_match

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return
    
def format_game_time(game_start_time):
    start_time = datetime.fromtimestamp(game_start_time / 1000) + timedelta(seconds=30)

    current_time = datetime.now()
    time_difference = current_time - start_time

    total_seconds = time_difference.total_seconds()

    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)

    time_string = "{:02d}:{:02d}".format(minutes, seconds)

    return str(time_string)
    

def get_game_time(start_time_epoch):
    # Get the current time in seconds
    current_time = time.time()
    
    # Calculate the elapsed time in seconds
    elapsed_time = current_time - start_time_epoch
    
    # Calculate minutes and seconds
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    # Format the time as a string with leading zeros
    time_string = "{:02d}:{:02d}".format(minutes, seconds)
    
    return time_string
