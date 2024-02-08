import requests
import time

# def time_since_last_match(player_last_match, api_key):
#     try:
#         player_match_data = f'https://americas.api.riotgames.com/lol/match/v5/matches/{player_last_match}?api_key={api_key}'
#         response = requests.get(player_match_data)

#         if response.status_code == 200:
#             player_specific_match = response.json()

#             match_start_time = player_specific_match['info']['gameStartTimestamp'] / 1000
#             game_duration = player_specific_match['info']['gameDuration']

#             current_time = time.time()

#             time_difference = current_time - (match_start_time + game_duration)

#         if time_difference < 60:  # Less than a minute
#             return f"{int(time_difference)} seconds ago", player_specific_match
#         elif time_difference < 3600:  # Less than an hour
#             minutes = int(time_difference / 60)
#             return f"{minutes} minute{'s' if minutes != 1 else ''} ago", player_specific_match
#         elif time_difference < 86400:  # Less than a day
#             hours = int(time_difference / 3600)
#             return f"{hours} hour{'s' if hours != 1 else ''} ago", player_specific_match
#         elif time_difference < 2592000:  # Less than a month (30 days)
#             days = int(time_difference / 86400)
#             return f"{days} day{'s' if days != 1 else ''} ago", player_specific_match
#         else:  # More than a month
#             months = int(time_difference) // (30 * 86400)
#             return f"{months} month{'s' if months != 1 else ''} ago", player_specific_match

#     except requests.exceptions.RequestException as e:
#         print(f"Error: {e}")
#         return
    

# def get_game_time(start_time_epoch):
#     # Get the current time in seconds
#     current_time = time.time()
    
#     # Calculate the elapsed time in seconds
#     elapsed_time = current_time - start_time_epoch
    
#     # Calculate minutes and seconds
#     minutes = int(elapsed_time // 60)
#     seconds = int(elapsed_time % 60)
    
#     # Format the time as a string with leading zeros
#     time_string = "{:02d}:{:02d}".format(minutes, seconds)
    
#     return time_string



# def current_game_status(player_data, api_key):
#     try:
#         player_game_status = f'https://na1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{player_data['id']}?api_key={api_key}'
#         response = requests.get(player_game_status)
#         if response.status_code == 200:
#             players_status = response.json()
#             return players_status, "IN GAME"
#         else:
#             # last game performane 
#             return time_since_last_match(player_data['match_id0'], api_key), "NOT IN GAME"
#     except requests.exceptions.RequestException as e:
#         print(f"Error: {e}")
#         return


