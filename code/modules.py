import requests
import time
import json
import os

from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup


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

    # Get today's date in UTC
    today_utc = datetime.now(timezone.utc).date()

    # Get the start of the day
    start_of_day_utc = datetime.combine(today_utc, datetime.min.time(), tzinfo=timezone.utc)

    # Get the end of the day
    end_of_day_utc = datetime.combine(today_utc, datetime.max.time(), tzinfo=timezone.utc)

    # Convert to epoch timestamps
    start_epoch_utc = int(start_of_day_utc.timestamp())
    end_epoch_utc = int(end_of_day_utc.timestamp())

    player_matches_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{summoner_puuid['puuid']}/ids?startTime={start_epoch_utc}&endTime={end_epoch_utc}&type=ranked&start=0&count=40&api_key={api_key}"
    
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
