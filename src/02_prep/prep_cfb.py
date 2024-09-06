import os
import pickle
from datetime import time, date

from pydantic import BaseModel

from cfp_model import League, Season, Team

# TODO make asssets dir this more genrally available via a constants scricpt??
assets_dir = os.path.join(os.getcwd().split('sports_sim')[0], 'sports_sim/assets/cfb') 

with open(os.path.join(assets_dir, 'season_ratings.pickle'), 'rb') as read_file:
    season_ratings = pickle.load(read_file)
    
# ---> Aggregate Season in a CFB League with Team and Conference alignments
'''
Construct the Division 1 team list from ratings, this information
also has the conference affiliation information as well as starting 
srs values for modeling if needed.
'''
league = League(seasons=[])
for team in season_ratings:
    league = league.add_team(Team.model_validate(team))
 
for season in league.seasons:
    print(f'{season.playoffs}')
    
        
        
# ---> What do we neeed to prep/clean/check/validate?  
# ---> What do we neeed to prep?  
# ---> What do we neeed to prep?  
# ---> What do we neeed to prep?  
# ---> What do we neeed to prep?  
# ---> What do we neeed to prep?  
# ---> What do we neeed to prep?  
# ---> What do we neeed to prep?  
# ---> What do we neeed to prep?  
# ---> What do we neeed to prep?  