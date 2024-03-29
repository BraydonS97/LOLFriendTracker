from os import execlpe
from flask import request
import requests
import html_update
import modules

AMERICAS_API_BASE_URL = 'https://americas.api.riotgames.com'
NA1_API_BASE_URL = 'https://na1.api.riotgames.com'

def get_summoner_id(gameName, tagLine, api_key):
    summoner_url = f"{AMERICAS_API_BASE_URL}/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}"
    response = requests.get(summoner_url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Returns AccID, ProfIconID, summonerID, puuid, summonerLevel
def get_summoner_data(summoner_puuid, api_key):
    summoner_info_url = f"{NA1_API_BASE_URL}/lol/summoner/v4/summoners/by-puuid/{summoner_puuid}?api_key={api_key}"
    response = requests.get(summoner_info_url)
    response.raise_for_status()
    return response.json()

# Returns RANK, WINS, LOSSES
def get_player_rank_data(summoner_id, api_key):
    player_current_rank_url = f"{NA1_API_BASE_URL}/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}"
    response = requests.get(player_current_rank_url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


def get_player_match_history(summoner_puuid, api_key):
    player_matches_url = f"{AMERICAS_API_BASE_URL}/lol/match/v5/matches/by-puuid/{summoner_puuid}/ids?type=ranked&start=0&count=30&api_key={api_key}"
    response = requests.get(player_matches_url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()


def get_player_game_status(player_data, api_key):
    try:    
        player_matches_url = f'https://na1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{player_data['id']}?api_key={api_key}'
        response = requests.get(player_matches_url)

        games_played_today = modules.games_played_today(player_data, api_key)
        
        if response.status_code == 200:
            player_game_status = response.json()

            return player_game_status, games_played_today, "IN GAME"
        else:
            return modules.time_since_last_match(player_data['match_id0'], api_key), games_played_today, "NOT IN GAME"
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

def retrieve_player_data(gameName, tagLine, api_key):
    try:
        summoner_info = get_summoner_id(gameName, tagLine, api_key)
        summoner_data = get_summoner_data(summoner_info['puuid'], api_key)
        player_ranked_data = get_player_rank_data(summoner_data['id'], api_key)

        # Formats match history into appropriate format to merge
        formatted_match_history = {}
        for i, entry in enumerate(get_player_match_history(summoner_info['puuid'], api_key)):
            key = f"match_id{i}"
            formatted_match_history[key] = entry

        # Merge data
        summoner_info.update(summoner_data)
        for player_rank_data_entry in player_ranked_data:
            summoner_info.update(player_rank_data_entry)
        for key, value in formatted_match_history.items():  # Iterate over key-value pairs
            summoner_info[key] = value  # Update summoner_info with match history data

        html_update.player_basic_banner(summoner_info)
        html_update.player_game_status_banner(summoner_info, get_player_game_status(summoner_info, api_key))
        
        return summoner_info
    
    except requests.exceptions.RequestException as e:
        print("Error: ", e)
        return None 