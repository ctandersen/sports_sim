'''
This script directs the webscraping of https://www.sports-reference.com/ for various models, starting with college football

College football has three main data sources 1. Schedules (i.e., game logs), 2. Conference Standings and 3. Team Ratings (and other information)
'''

import os
import sys

import pickle
from cfb.scrape_cfb import get_season_ratings, get_season_schedule, get_season_standings, get_season_polls

def scrape_cfb(rerun_historical: bool, historical_seasons: list[int], current_season: list[int]) -> None:
    pass

# ---> Settings
rerun_historical = False
include_polls = True
poll_seasons = list(range(2019, 2024)) 

# TODO change this to 1986, 2024 after developed
historical_seasons = list(range(2019, 2024)) 
current_season = [2024]

# ---> Scrape new data
# check what seasons we are running, all historical or just current from rerun_historical bool
if rerun_historical:
    seasons = historical_seasons
    seasons.extend(current_season)
else:
    seasons = current_season

#TODO understand this comprehension better
season_ratings = [fetched for season in seasons for fetched in get_season_ratings(season)] 
season_standings = [fetched for season in seasons for fetched in get_season_standings(season)]
season_schedule = [fetched for season in seasons for fetched in get_season_schedule(season)]
    
# ---> Load previous data
assets_dir = os.path.join(os.getcwd().split('sports_sim')[0], 'sports_sim/assets/cfb') 

with open(os.path.join(assets_dir, 'season_ratings.pickle') , 'rb') as read_file:
    season_ratings_previous = pickle.load(read_file)

with open(os.path.join(assets_dir, 'season_standings.pickle'), 'rb') as read_file:
    season_standings_previous = pickle.load(read_file)

with open(os.path.join(assets_dir, 'season_schedule.pickle'), 'rb') as read_file:
    season_schedule_previous = pickle.load(read_file)



# ---> Remove seasons in current scrape
season_ratings_cleaned = [ x for x in season_ratings_previous if int(x['season']) not in seasons ]
season_standings_cleaned = [ x for x in season_standings_previous if int(x['season']) not in seasons ]
season_schedule_cleaned = [ x for x in season_schedule_previous if int(x['season']) not in seasons ]

# ---> Add previous scrape to current scrape and then sort 
# Sorting by season is mostly for convenience
season_ratings.extend(season_ratings_cleaned)
season_ratings.sort(key=lambda team: team['season'])

season_standings.extend(season_standings_cleaned)
season_standings.sort(key=lambda team: team['season'])

season_schedule.extend(season_schedule_cleaned)
season_schedule.sort(key=lambda game: game['season'])



# ---> Save pickle files
with open(os.path.join(assets_dir, 'season_ratings.pickle'), 'wb') as write_file:
    pickle.dump(season_ratings, write_file, protocol=pickle.HIGHEST_PROTOCOL)

with open(os.path.join(assets_dir, 'season_standings.pickle'), 'wb') as write_file:
    pickle.dump(season_standings, write_file, protocol=pickle.HIGHEST_PROTOCOL)

with open(os.path.join(assets_dir, 'season_schedule.pickle'), 'wb') as write_file:
    pickle.dump(season_schedule, write_file, protocol=pickle.HIGHEST_PROTOCOL)

# ---> Doing Polls seperate for now
if include_polls:
    season_polls = [fetched for season in poll_seasons for fetched in get_season_polls(season)]
        
    with open(os.path.join(assets_dir, 'season_polls.pickle'), 'rb') as read_file:
        season_polls_previous = pickle.load(read_file)

    season_polls_cleaned = [ x for x in season_polls_previous if int(x['season']) not in poll_seasons ]
    season_polls.extend(season_polls_cleaned)
    season_polls.sort(key=lambda game: game['season'])

    with open(os.path.join(assets_dir, 'season_polls.pickle'), 'wb') as write_file:
        pickle.dump(season_polls, write_file, protocol=pickle.HIGHEST_PROTOCOL)

# ---> Logging and print success
# TODO Adding logging to this script
print('\033[94m' + f'Pickle files are saved in {assets_dir}. Scrape is Complete!' + '\033[0m')

